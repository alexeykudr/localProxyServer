from distutils.command.config import config


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
        "users apple:CL:pen\n",
        f"users {self.user_login}:CL:{self.user_password}\n",
        f"allow apple,{self.user_login}\n",
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
# cat 3proxy12.cfg
# Configurator(22, "el", "pablito").writeConfig()