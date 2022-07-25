from flask import Flask
from flask import request
from proxyapi import ProxyApi
import os
app = Flask(__name__)


@app.route("/")
def hello():
    return {"Ok": "True"}


@app.route('/updatePortInterval/', methods=['GET'])
def updatePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        interval = request.args.get('interval')
        print(f"Add new job to crontab with port:{id}, interval:{interval}")
        if id and interval:
            router_api.newJob(id, interval)
            return {id: interval}

        return {"Message": "Error"}


@app.route('/removePortInterval/', methods=['GET'])
def removePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            router_api.removeJob(id)
            return {"id": id}

        return {"Message": "Error"}


@app.route('/rebootPort/', methods=['GET'])
def rebootPort():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            print('Modem reloading by url {}'.format(id))
            ip1, ip2 = router_api.rebootRouter(id)
            return {"Ip is change!": f"Before {ip1} , after {ip2}"}

        return {"Message": "Error"}

@app.route('/setConfig', methods=['POST'])
def setConfig():
    if request.method == 'POST':
        portId = int(request.values.get('id'))
        if portId is None:
            return {"Message": "Bad id!"}
        
        username = request.values.get('username')
        if username is None:
            return {"Message": "Bad username!"}
        
        password = request.values.get('password') # input names
        
        if password is None:
            return {"Message": "Bad password!"}
        
        if username == 'auto' and password == 'auto':
            username = router_api.get_random_string(8)
            password = router_api.get_random_string(8)
            
        try:
            router_api.createProxyConfig(portId, username, password)
        except Exception as e:
            return {portId: f'{username}, {password}'}

        return {portId: f'{username}, {password}'}


if __name__ == "__main__":
    router_api = ProxyApi()

    port = int(os.environ.get("PORT", 8081))
    app.run(debug=False, host='0.0.0.0', port=port)

    # // TODO get ip adres bellow reload and after (python logic) and log this (python logic)
    # // TODO compare ip addr , want to get uniq addr
    # // TODO generate random log pass
