import requests
import sys

def getPortsUrl(ip,port):
    portString = ''
    if type(port) is list:
        portString+=port[0]
        for index in range(1,len(port)):
            portString = portString + '%0A'+port[index]
    else:
        portString+=port
    porturl = f"http://{ip}:20080/NMSRequest/GetObjects?NoHTML=true&Objects={portString}"
    return porturl

def getResponse(ip,port):
    session = requests.Session()
    session.auth = ('tejas', 'j72e#05t')
    session.headers.update({"Cookie": "LOGIN_LEVEL=2; path=/;"})
    try:
        r = session.get(getPortsUrl(ip,port))
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    response = r.text
    return response

def getPortStatus(ip,port):

    if port.startswith('SFP'):
        key = '-OperStatus'
        value = 'up'
    elif port.startswith('Port'):
        key = '-ifOperStatus'
        value = 'if_oper_up'
    elif port.startswith('ONTGEthPort-'):
        key = '-OperationalState'
        value = 'os_enable'

    response = getResponse(ip,port)
    responseLines = response.split('\n')[1:-1]
    for line in responseLines:
        values = line.split('\t')
        if port == values[0]:
            for index in range(0, len(values), 2):
                    if values[index]==key:
                        return 1 if values[index+1] == value else 2

print(getPortStatus(sys.argv[1],sys.argv[2]))
