import sqlite3
from turtle import ht
import requests
import urllib3

urllib3.disable_warnings()

conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()
# res = cur.execute('SELECT router_id FROM proxyPorts where pass NOT IN (?)', ('None', )).fetchall()
res = cur.execute(
    'SELECT router_id, user_login, pass, generatedUrl from proxyPorts').fetchall()

response = requests.get("https://ipinfo.io/ip", verify=False)
local_ip = response.text

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
    


