import requests
import urllib3

urllib3.disable_warnings()


def getIp(proxy_list) -> str:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET '
                        'CLR 3.5.30729)'}
        for proxy in proxy_list:   
            print(f'Start checking ip! proxy: {proxy}')
            formated = [proxy.split(":")]
            proxy_data = formated[0]
            proxy_dict = {'https': 'http://{}:{}@{}:{}'.format(proxy_data[2],
                                                            proxy_data[3],
                                                            proxy_data[0],
                                                            proxy_data[1])}
            try:
                response = requests.get("https://ipinfo.io/ip", headers=headers, proxies=proxy_dict, verify=False)
                return response.text
            except Exception as e:
                print(e)
                
ip1 = getIp(["46.227.245.119:7012:mama:stiflera"])
print(ip1)