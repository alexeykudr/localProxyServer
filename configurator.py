class Configurator():
    def __init__(self, portId:int, user_login, user_password) -> None:
        self.portId = portId
        self.user_login = user_login
        self.user_password = user_password
        self.config = ["daemon\n",
            "timeouts 1 5 30 60 180 1800 15 60\n",
            "maxconn 5000\n",
            "nscache 65535\n",
            f"nserver 192.168.{self.portId}.1\n",
            f"log /usr/local/3proxy/mob/log/server199-192.168.{self.portId}.100.log D\n",
            "logformat L%C - %U - %e [%d/%o/%Y:%H:%M:%S %z] %N.%p ""%T"" %E %I %O %N/%R:%r\n",
            "rotate 360\n",
            "archiver rar rar a -df -inul %A %F\n",
            "auth iponly strong\n",
         # technical proxy
            "users 786691447:CL:3232235686\n",
            "users checkermob:CL:3jSpXRv4HqUd\n",
            "allow 786691447,checkermob\n",
            #proxy -s0 -n -a -p9011 -i192.168.0.166 -e192.168.11.100
            f"proxy -s0 -n -a -p9011 -i0.0.0.0 -e192.168.{self.portId}.100\n",
            "flush\n",
            "connlim 200 0 6c69dc0a9e\n",
            "auth strong\n",
            "bandlimin 15000000 6c69dc0a9e\n",
            "bandlimout 15000000 6c69dc0a9e\n",
            f"users {self.user_login}:CL:{self.user_password}\n",
            f"deny {self.user_login} * $/usr/local/3proxy/banlist61.list * * *\n",
            f"allow {self.user_login} * * * * * *",
            f"proxy -s0 -n -a -p41805 -i0.0.0.0 -e192.168.{self.portId}.100\n",
            f"socks -s0 -n -a -p42711 -i0.0.0.0 -e192.168.{self.portId}.100\n",
            #monitor /usr/local/3proxy/banlist61.list
            "flush\n"]
        # print(self.config)
        
        
    def writeConfig(self):
        file_path =f"/usr/local/3proxy/mob/3proxy{self.portId-10}.cfg"
        # file_path = 'sample.cfg'
        with open (file_path, 'w+') as example_conf:
            for line in self.config:
                example_conf.writelines(line) 
        