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
        print(id, interval)
        if id and interval:
            router_api.newJob(id, interval)
            return {id: interval}

        return {"Message": "Bad request!"}


@app.route('/removePortInterval/', methods=['GET'])
def removePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            router_api.removeJob(id)
            return {"id": id}

        return {"Message": "Bad request!"}


@app.route('/rebootPort/', methods=['GET'])
def rebootPort():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            #  need log this
            # get ip
            print('want reboot {}'.format(id))
            router_api.rebootRouter(id)
            # get ip
            # check if == then .rebootRouter
            return {"id": id}

        return {"Message": "Bad request!"}

@app.route('/setConfig', methods=['POST'])
def setConfig():
    if request.method == 'POST':
        portId = int(request.values.get('id'))
        if portId is None:
            return {"Message": "Bad request!"}
        
        username = request.values.get('username') # Your form's
        password = request.values.get('password') # input names
        
        if username == 'auto' and password == 'auto':
            username = router_api.get_random_string(8)
            password = router_api.get_random_string(8)
            
        router_api.createProxyConfig(portId, username, password)

        return {portId: f'{username}, {password}'}


if __name__ == "__main__":
    router_api = ProxyApi()

    port = int(os.environ.get("PORT", 8081))
    app.run(debug=True, host='0.0.0.0', port=port)

    # // TODO get ip adres bellow reload and after (python logic) and log this (python logic)
    # // TODO compare ip addr , want to get uniq addr
    # // TODO generate random log pass
