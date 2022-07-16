from crontab import CronTab
import sys
import os
# https://pypi.org/project/python-crontab/

class CronJob():
    def __init__(self) -> None:
        self.username = os.getlogin()
        self.cron = CronTab(user=self.username)

    def newJob(self, portId: int, interval: int) -> None:
        self.query_command = "/usr/bin/flock -w 0 /var/run/192.168.{}.100.lock /home/mac/proxyHobbit/reconnect.sh -r 4G  -i 192.168.{}.1 /etc/init.d/3proxy start192.168.{}.1 >/dev/null 2>&1".format(
            portId, portId, portId)
        self.job = self.cron.new(command=self.query_command, comment=str(portId))
        self.job.minute.every(interval)
        self.cron.write()
        
    def job_stop(self):
        self.job.enable(False)
        self.cron.remove(self.job)
        # job.enable(False)
        
    def iter(self):
        for job in self.cron:
            print(job)
            
    def removeJob(self, portId):
        iter = self.cron.find_command(str(portId))
        self.cron.remove(iter)
        self.cron.write()

if __name__ == "__main__":
    
    c= CronJob()
    # python3 cron.py -add 15 25
    # python3 cron.py -rm 15 
    if sys.argv[1] == '-add':
        if sys.argv[2] and sys.argv[3]:
            # add job port id interval
             c.newJob(sys.argv[2], sys.argv[3])
    if sys.argv[1] == '-rm':
        if sys.argv[2]:
            c.removeJob(sys.argv[2])