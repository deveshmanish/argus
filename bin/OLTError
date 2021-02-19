import requests
import sys

def transformPortName(port):

    if port.startswith('Port_Eth'):
        text = port.split('-')
        text[0] = 'ETH'
        text.pop(1)
        port = '-'.join(text)

    return port


def getPortsStatsUrl(ip,port,interval=0,start=0,last=0):
    portString = ''
    if type(port) is list:
        portString+=port[0]
        for index in range(1,len(port)):
            portString = portString + '%0A'+port[index]
    else:
        portString+=port
    porturl = f"http://{ip}:20080/NMSRequest/IntervalStats?NoHTML=true&Objects={portString}&Start={start}&Last={last}&Type={interval}"
    return porturl

def getOpticalResponse(ip,port):
    session = requests.Session()
    session.auth = ('tejas', 'j72e#05t')
    session.headers.update({"Cookie": "LOGIN_LEVEL=2; path=/;"})
    try:
        r = session.get(getPortsStatsUrl(ip,port))
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    response = r.text
    return response

def getOpticalPower(ip,port,key='-RxPower'):

    if port.startswith('SFP'):
        key = '-RxPower'
    elif port.startswith('Port_GPON'):
        key = '-rxCrcErrors'
    elif port.startswith('ONTGEthPort-'):
        key = '-onuEthPortPmRxFcsErrors'
    else:
        key = '-ES'
    response = getOpticalResponse(ip,port)
    responseLines = response.split('\n')[1:-1]
    for index in range(0, len(responseLines), 3):
        item = responseLines[index].split('\t')[0]
        keyItems = responseLines[index + 1].split('\t')[1:]
        valueItems = responseLines[index + 2].split('\t')[1:]
        if port==item:
            for keyItem, valueItem in zip(keyItems, valueItems):
                if keyItem==key:
                    return valueItem

print(getOpticalPower(sys.argv[1],sys.argv[2]))
