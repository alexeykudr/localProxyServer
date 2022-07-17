from flask import Flask
from flask import request
import os
from crontab import CronTab
import subprocess

# https://pypi.org/project/python-crontab/

class CronJob():
    def __init__(self) -> None:
        self.user_login = os.environ["USER"]
        self.cron = CronTab(user=self.user_login) 

    def newJob(self, portId: int, interval: int) -> None:
        self.query_command = "/usr/bin/flock -w 0 /var/run/192.168.{}.100.lock /home/mac/localProxyServer/reconnect.sh -r 4G  -i 192.168.{}.1 /etc/init.d/3proxy start192.168.{}.1 >/dev/null 2>&1".format(
            portId, portId, portId)
        self.job = self.cron.new(command=self.query_command, comment=str(portId))
        self.job.minute.every(interval)
        self.cron.write()
        
    def job_stop(self):
        self.job.enable(False)
        self.cron.remove(self.job)
        
    def iter(self):
        for job in self.cron:
            print(job)
            
    def removeJob(self, portId):
        iter = self.cron.find_comment(str(portId))
        self.cron.remove(iter)
        self.cron.write()

class Rebooter():
    def __init__(self) -> None:
        self.user_login = os.environ["USER"]
        
    def rebootRouter(self, id):
        result = subprocess.run(["/bin/bash", "/home/{}/localProxyServer/reload.sh".format(self.user_login), 
                                 "{}".format(id)],
                        timeout=15, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result


app = Flask(__name__)
@app.route("/")
def hello():
    return {"Ok":"True"}

@app.route('/updatePortInterval/', methods=['GET'])
def updatePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        interval = request.args.get('interval')
        print(id, interval)
        if id and interval:
            cron_object.newJob(id, interval)
            return {id:interval}
        
        return {"Message":"Bad request!"}

@app.route('/removePortInterval/', methods=['GET'])
def removePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            cron_object.removeJob(id)
            return {"id": id}
        
        return {"Message":"Bad request!"}

@app.route('/rebootPort/', methods=['GET'])
def rebootPort():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            print('want reboot {}'.format(id))
            rebooter_object.rebootRouter(id)
            return {"id": id}
        
        return {"Message":"Bad request!"}
    
    
if __name__ == "__main__":
    cron_object = CronJob()
    rebooter_object = Rebooter()
    # python3 cron.py -add 15 25
    # 15 - portId , 25 - interval
    port = int(os.environ.get("PORT", 8081))
    app.run(debug=True,host='0.0.0.0',port=port)
    
