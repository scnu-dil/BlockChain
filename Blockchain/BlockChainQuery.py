import requests

"""
bubi区块链信息查询工具
author：mxd
"""

"""
0 发送http get请求
"""
def sendGet(url,param):
    for i in range(10):
        try:
            str_url = url+"?"+param
            print('url:%s' %str_url)
            res = requests.get(str_url, timeout=5)
            return res.json()
        except Exception as e:
            print(e)
            import time
            time.sleep(1)
            continue

"""
1.1 查询账户1
    ip
    address
"""
def getAccount1(ip,address):
    url = "http://"+ip+"/getAccount"
    param = "address="+address
    return sendGet(url,param)
"""
1.2 查询账户2
    ip
    address
    key: metadata 中指定的key的值，如果不填写，那么返回结果中含有所有的metadata
"""

def getAccount2(ip,address,key):
    url = "http://" + ip + "/getAccount"
    param = "address=" + address+"&key="+key
    return sendGet(url, param)
"""
1.3 查询账户3
    ip
    address
    key: metadata 中指定的key的值，如果不填写，那么返回结果中含有所有的metadata
    code: 资产代码
    issuer: 资产发行商，这两个变量要么同时填写，要么同时不填写。若不填写，返回的结果中包含所有的资产。若填写，返回的结果中只显示由code和issuer指定的资产。   
"""
def getAccount3(ip,address,key,code,issuer):
    url = "http://" + ip + "/getAccount"
    param = "address=" + address+"&key="+key+"&code="+code+"&issuer="+issuer
    return sendGet(url, param)
"""
1.4 获取账号nonce值
    ip
    address
"""
def getAccountNonce(ip,address):
    nonce = -1
    res = getAccount1(ip,address)
    if res['error_code'] ==0:
        nonce =res['result']['nonce']
    return  nonce
"""
1.5 获取账号资产信息
    ip
    address
"""
def getAccountAssets(ip,address):
    res = getAccount1(ip,address)
    if res['error_code'] is 0:
        assets =res['result']['assets']
    return  assets
"""
1.6 获取账号资产数量
    ip
    address
    code: 
"""
def getAccountAssetsAmount(ip,address,code):
    assets = getAccountAssets(ip,address)
    print(assets)
    for e in assets:
        code_type = e['property']
        if code_type['code'] == code:
            amount = e['amount']
    return amount
"""
2.1 查询交易1
    ip
    hash
"""
def getTransactionHistory1(ip,hash):
    url = "http://" + ip + "/getTransactionHistory"
    param = "hash=" + hash
    return sendGet(url, param)
"""
2.2 查询交易3
    ip
    ledger_seq: 查询指定区块中的所有交易
"""
def getTransactionHistory2(ip,ledger_seq):
    url = "http://" + ip + "/getTransactionHistory"
    param = "address=" + address + "&ledger_seq=" + ledger_seq
    return sendGet(url, param)
"""
3.1 查询区块头1
    ip
    seq： ledger的序号， 如果不填写，返回当前ledger
    with_validator： 默认false，不显示验证节点列表
    with_consvalue: 默认false，不显示共识值
"""
def getLedger1(ip,seq,with_validator,with_consvalue):
    url = "http://" + ip + "/getLedger"
    param = "address=" + address + "&seq=" + seq +"&with_validator=" + with_validator +"&with_consvalue=" +with_consvalue
    return sendGet(url, param)
"""
3.2 查询区块头2
    ip
"""
def getLedger2(ip):
    url = "http://" + ip + "/getLedger"
    param = ""
    return sendGet(url, param)
"""
4 获取区块链详情
    ip
"""
def getModulesStatus(ip):
    url = "http://" + ip + "/getModulesStatus"
    param = ""
    return sendGet(url, param)





if __name__ == '__main__':
    ip = "192.168.0.201:29334"
    address = "a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18"
    code = "test"
    print(getAccount1(ip,address))