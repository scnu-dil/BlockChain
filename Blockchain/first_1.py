import requests
import json
"""
1：把每一个接口操作都封装好
2：数据分析，主函数调用接口
"""
#获取带有请求参数的url地址
def getUrl(url,param):
    with open('./params_for_get.json') as f:
        elements = json.load(f)[param]
        url = url + '/'+param+'?'
        for e in elements:
            v =elements[e]
            url = url + '%s'%e+'=%s'%v+'&'
    return url
#查询区块详情
def getModulesStatus(url):
    param = 'getModulesStatus'
    url = getUrl(url, param)
    res = requests.get(url)
    return res.json()
#查询区块头
def getLedger(url):
    param = 'getLedger'
    url = getUrl(url,param)
    res = requests.get(url)
    return res.json()
#查询账户
def getAccount(url,sourceAddress):
    param = 'getAccount'
    url = getUrl(url, param)
    res = requests.get(url)
    return res.json()
#查询交易
def getTransactionHistory(url):
    param = 'getTransactionHistory'
    url = getUrl(url, param)
    res = requests.get(url)
    return res.json()
#创建密钥对
def createAccount(url):
    param = 'createAccount'
    url = getUrl(url, param)
    res = requests.get(url)
    return res.json()



#获取nonce数值
def getnonce(url,sourceAddress):
    nonce = -1
    res = getAccount(url,sourceAddress)
    if res['error_code'] == 0:
        nonce =res['result']['nonce']
    return  nonce

#交易1：序列化
"""
参数1：url
参数2：交易的发起方账号地址
参数3：表达式字段
参数4：操作
"""
def getTransactionBlob(url,sourceAddress,exprCondition,operations):
    nonce = getnonce(url,sourceAddress)+1
    if nonce == 0:
        print("交易账号："+sourceAddress+",交易数异常，nonce="+nonce+",交易中断！")
        return
    res = Transaction(url,sourceAddress,nonce,exprCondition,operations)
    return res['transaction_blob']
#交易
def Transaction(url,sourceAddress,nonce,exprCondition,operations):
    pass

#之创建账号
def create_account_blob(url):
    with open('./params_for_post.json',encoding='gb18030') as f:
        data = json.load(f)['type1']
    url = url+'/getTransactionBlob'
    res = requests.post(url, json=data)
    return res.text
#序列化交易之发行资产
def issue_asset_blob(url):
    with open('./params_for_post.json',encoding='gb18030') as f:
        data = json.load(f)['type2']
    url = url+'/getTransactionBlob'
    res = requests.post(url, json=data)
    return res.text
#序列化交易之转移资产
def payment_asset_blob(url):
    with open('./params_for_post.json',encoding='gb18030') as f:
        data = json.load(f)['type3']
    url = url+'/getTransactionBlob'
    res = requests.post(url, json=data)
    return res.text
#序列化交易之设置数据
def set_metadata_blob(url):
    with open('./params_for_post.json',encoding='gb18030') as f:
        data = json.load(f)['type4']
    url = url+'/getTransactionBlob'
    res = requests.post(url, json=data)
    return res.text
#提交交易
def submitTransaction(url):
    with open('./params_for_post.json',encoding='gb18030') as f:
        data = json.load(f)['type0']
    url = url+'/submitTransaction'
    res = requests.post(url, json=data)
    return res.text
if __name__ == '__main__':
    url = 'http://192.168.0.201:29334'
    sourceAddress = 'a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18'
    getnonce(url, sourceAddress)


