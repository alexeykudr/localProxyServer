import json
import os
from urllib import response
from crontab import CronTab
import subprocess
import random
import string
import requests


class Configurator():
    def __init__(self, portId:int, user_login, user_password) -> None:
        self.portId = portId
        self.user_login = user_login
        self.user_password = user_password
        self.config = [
        "daemon\n",
        "timeouts 1 5 30 60 180 1800 15 60\n",
        "maxconn 5000\n",
        f"nserver 192.168.{self.portId}.1\n",
        "nscache 65535\n",
        "log /dev/null\n",
        "auth iponly strong\n",
        "users mama:CL:stiflera\n",
        f"users {self.user_login}:CL:{self.user_password}\n",
        f"allow mama,{self.user_login}\n",
        "allow * 8.8.8.8,2.2.2.2 * * * * * \n",
        f"proxy -n -a -p70{self.portId-10} -i192.168.0.167 -e192.168.{self.portId}.100\n",
        f"socks -n -a -p80{self.portId-10} -i192.168.0.167 -e192.168.{self.portId}.100\n",
        "flush\n"
        ]
        
        
        
    def writeConfig(self):
        # /usr/local/3proxy/mob/
        file_path =f"/usr/local/3proxy/mob/3proxy{self.portId-10}.cfg"
        # file_path = 'sample.cfg'
        with open (file_path, 'w+') as example_conf:
            for line in self.config:
                example_conf.writelines(line)
        ult = os.system("/home/mac/reload_service.sh")
        #result = subprocess.run(["sudo /bin/bash", "/home/{}/reload_service.sh".format(self.user_login),
         #                        "{}".format(id)],
          #                      timeout=5, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
class ProxyApi():
    # Api to reboot router by reload sh script, add job to cron which give reloading every N min.
    def __init__(self) -> None:
        self.user_login = os.environ["USER"]
        self.cron = CronTab(user=self.user_login)

    def rebootRouter(self, id):
        # todo
        # want get ip addr bellow reload , it will be string
        # response_dict = dict()
        # response_dict["current_ip"] = self.getRouterIp(id)
        ult = os.system(f"/home/{self.user_login}/reload.sh {id}")
    #    result = subprocess.run(["sudo /bin/bash", "/home/{}/reload.sh".format(self.user_login),
     #                            "{}".format(id)],
      #                          timeout=25, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # response_dict["ip after change"] = self.getRouterIp(id)
        # print(response_dict)
        
        
    def newJob(self, portId: int, interval: int) -> None:
        self.query_command = f"/usr/bin/flock -w 0 /var/run/192.168.{portId}.100.lock /home/{self.user_login}/reconnect.sh -r 4G  -i 192.168.{portId}.1 /etc/init.d/3proxy start192.168.{portId}.1 >/dev/null 2>&1"
        # self.query_command = "/usr/bin/flock -w 0 /var/run/192.168.{}.100.lock /home/mac/reconnect.sh -r 4G  -i 192.168.{}.1 /etc/init.d/3proxy start192.168.{}.1 >/dev/null 2>&1".format(
        #     portId, portId, portId)
        self.job = self.cron.new(
            command=self.query_command, comment=str(portId))
        self.job.minute.every(interval)
        self.cron.write()

    def iter(self):
        for job in self.cron:
            print(job)

    def removeJob(self, portId):
        try:
            iter = self.cron.find_comment(str(portId))
            self.cron.remove(iter)
            self.cron.write()
        except Exception as err:
            print("Error in remove job! ", err.args)

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def getRouterIp(self, portId: str):
        formated = [portId.split(":")]
        proxy_data = formated[0]
        proxies = {'https': 'http://{}:{}@{}:{}'.format(proxy_data[2],
                                                        proxy_data[3],
                                                        proxy_data[0],
                                                        proxy_data[1])}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET '
            'CLR 3.5.30729)'}
        with open('file.txt', 'a') as file:
            try:
                ipinfo_response = requests.get("https://ipinfo.io/ip",
                                               headers=headers, proxies=proxies, timeout=2)
                file.writelines(f'{ipinfo_response.text}\n')
                file.close()
            except Exception as e:
                ipinfo_response = requests.get("https://ipinfo.io/ip",
                                               headers=headers, proxies=proxies, timeout=2)
                file.writelines(f'{ipinfo_response.text}\n')
                file.close()
        print(ipinfo_response.text)
        return ipinfo_response.text

    def createProxyConfig(self, portId, user_log, user_pass):
        config = Configurator(portId, user_log, user_pass)
        config.writeConfig()
