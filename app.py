import sqlite3
from flask import Flask, jsonify, render_template
from flask import request
from proxyapi import ProxyApi
import os
from flask import Response
import json
import requests


app = Flask(__name__)


@app.route("/")
def hello():
    response = {}
    response['Message'] = "Work!"
    return Response(json.dumps(response), status=403, mimetype='application/json')


@app.route('/updateinterval', methods=['GET'])
def updatePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        key = request.args.get('key')
        interval = request.args.get('interval')
        
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        
        
        print(f"Add new job to crontab with port:{id}, interval:{interval}")
        if id and interval:
            router_api.newJob(id, interval)
            response = {}
            response['id'] = interval
            return Response(json.dumps(response), status=200, mimetype='application/json')

    return Response("{'Message':'Error'}", status=404, mimetype='application/json')
        


@app.route('/deleteinterval', methods=['GET'])
def removePortInterval():
    if request.method == 'GET':
        id = request.args.get('id')
        key = request.args.get('key')
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        
        if id:
            router_api.removeJob(id)
            response = {}
            response['Ok'] = id
            return Response(json.dumps(response), status=200, mimetype='application/json')

        return Response("{'Message':'Error'}", status=404, mimetype='application/json')


@app.route('/changeipID', methods=['GET'])
def rebootPort():
    if request.method == 'GET':
        id = request.args.get('id')
        key = request.args.get('key')
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        if id:
            print('Modem reloading by id {}'.format(id))
            ip1, ip2 = router_api.rebootRouter(id)
            response = {}
            response['IP сменился!'] = f"Прошлый IP {ip1}, Текущий {ip2}"
            return Response(json.dumps(response), status=200, mimetype='application/json')

            # return jsonify(dict(id = int(id) , ip_before=ip1, ip_after=ip2))

        return Response("{'Message':'Error'}", status=404, mimetype='application/json')



@app.route('/setConfig', methods=['GET'])
def setConfig():
    if request.method == 'GET':
        portId = int(request.values.get('id'))
        key = request.args.get('key')
        username = request.values.get('username')
        password = request.values.get('password')
        
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        
        if portId is None:
            response = {}
            response['Message'] = "Empty port id!"
            return Response(json.dumps(response), status=404, mimetype='application/json')

        
        if username is None:
            response = {}
            response['Message'] = "Empty username!"
            return Response(json.dumps(response), status=404, mimetype='application/json')

        if password is None:
            response = {}
            response['Message'] = "Empty password!"
            return Response(json.dumps(response), status=404, mimetype='application/json')

        if username == 'auto' and password == 'auto':
            username = router_api.get_random_string(8)
            password = router_api.get_random_string(8)

        try:
            router_api.createProxyConfig(portId, username, password)
            cur.execute('UPDATE proxyPorts SET user_login = ?, pass = ? where router_id = ?', (username, password, portId))
            conn.commit()
        except Exception as e:
            print(e)
            return {"Error with creation config": "check server logs"}


        return jsonify(dict(id=portId, username=username, password=password))


@app.route('/changeip/<name>')
def changeip(name):
    res = cur.execute('SELECT router_id FROM proxyPorts where generatedUrl = ?', (name, )).fetchall()
    try:
        id = res[0][0]
        ip1, ip2 = router_api.rebootRouter(id)
        # print(ip1, ip2)
        return render_template('ipchange.html', ip_before=ip1, ip_after=ip2)
        # return jsonify(dict(id = int(id) , ip_before=ip1, ip_after=ip2))
    except IndexError:
        print('try to change ip! But shit hapiens, name dont found')

    response = {}
    response['Wrong url'] = name
    return Response(json.dumps(response), status=404, mimetype='application/json')

@app.route('/generatelink', methods=['GET'])
def generateLink():
    if request.method == 'GET':
        id = request.args.get('id')
        key = request.args.get('key')
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        
        if id:
            random_string = ProxyApi.get_random_string(16)
            cur.execute('UPDATE proxyPorts SET generatedURL = ? where router_id = ?', (random_string, int(id)))
            conn.commit()
            response = {}
            response[id] = random_string
            return Response(json.dumps(response), status=200, mimetype='application/json')
        
        response = {}
        response['Error'] = "check server logs"
        return Response(json.dumps(response), status=404, mimetype='application/json')

@app.route('/getproxy', methods=['GET'])
def getproxy():
    if request.method == 'GET':
        key = request.args.get('key')
        if key != const_pass:
            response = {}
            response['Message'] = "Wrong password!"
            return Response(json.dumps(response), status=403, mimetype='application/json')
        
        # get server ip
        try:
            response = requests.get("https://ipinfo.io/ip", verify=False)
            local_ip = response.text      
        except Exception as e:
            print(e)
            
        # prepare proxy data
        res = cur.execute('SELECT router_id, user_login, pass, generatedUrl from proxyPorts').fetchall()
        http_proxy_dict = {}
        sock_proxy_dict = {}

        for i in res:
            portId = i[0]
            user_login = i[1]
            user_password = i[2]
            link = i[3]
            # http://46.227.245.119:8081/changeip/gmxgjpafvkpagsop
            http_proxy_str = f"{local_ip}:70{portId}:{user_login}:{user_password}"
            http_proxy_link = f"http://{local_ip}:8881/changeip/{link}"
            
            
            sock_proxy_str = f"{local_ip}:80{portId}:{user_login}:{user_password}"
            sock_proxy_link = f"http://{local_ip}:8881/changeip/{link}"
            
            
            # http_proxy.append(http_proxy_str)
            # socks_proxy.append(sock_proxy_str)
            http_proxy_dict[http_proxy_str] = http_proxy_link
            sock_proxy_dict[sock_proxy_str] = sock_proxy_link
            
        return render_template("getproxy.html", proxy = http_proxy_dict)
        

if __name__ == "__main__":
    const_pass = 'guccibeggins'
    router_api = ProxyApi()
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cur = conn.cursor()
    port = int(os.environ.get("PORT", 8881))
    app.run(debug=False, host='0.0.0.0', port=port)