import sqlite3
from flask import Flask, jsonify
from flask import request
from proxyapi import ProxyApi
import os
app = Flask(__name__)


@app.route("/")
def hello():
    return {"Ok": "True"}


@app.route('/updateinterval', methods=['GET'])
def updatePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        interval = request.args.get('interval')
        print(f"Add new job to crontab with port:{id}, interval:{interval}")
        if id and interval:
            router_api.newJob(id, interval)
            return jsonify({"id": interval})

        return {"Message": "Error"}


@app.route('/deleteinterval', methods=['GET'])
def removePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            router_api.removeJob(id)
            return jsonify({"id": id})

        return {"Message": "Error"}


@app.route('/changeipID', methods=['GET'])
def rebootPort():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            print('Modem reloading by id {}'.format(id))
            ip1, ip2 = router_api.rebootRouter(id)
            print(ip1, ip2)
            return jsonify(dict(id = int(id) , ip_before=ip1, ip_after=ip2))

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

        password = request.values.get('password')  # input names

        if password is None:
            return {"Message": "Bad password!"}

        if username == 'auto' and password == 'auto':
            username = router_api.get_random_string(8)
            password = router_api.get_random_string(8)

        try:
            router_api.createProxyConfig(portId, username, password)
        except Exception as e:
            return {"Message": "Error"}

        return jsonify(dict(id=portId, username=username, password=password))


@app.route('/changeip/<name>')
def changeip(name):
    res = cur.execute('SELECT router_id FROM proxyPorts where generatedUrl = ?', (name, )).fetchall()
    try:
        id = res[0][0]
        print('Modem reloading by id {}'.format(id))
        ip1, ip2 = router_api.rebootRouter(id)
        print(ip1, ip2)
        return jsonify(dict(id = int(id) , ip_before=ip1, ip_after=ip2))
    except IndexError:
        print('try to change ip! But shit hapiens, name dont found')
    conn.close()

    return name

@app.route('/generatelink', methods=['GET'])
def generateLink():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            random_string = ProxyApi.get_random_string(16)
            cur.execute('UPDATE proxyPorts SET generatedURL = ? where id = ?', (random_string, int(id)))
            conn.commit()
            conn.close()
            return {id:random_string}

        return {"Message": "Error"}

if __name__ == "__main__":
    router_api = ProxyApi()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    port = int(os.environ.get("PORT", 8081))
    app.run(debug=False, host='0.0.0.0', port=port)