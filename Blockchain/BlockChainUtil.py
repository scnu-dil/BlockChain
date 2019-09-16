import json

from Blockchain.BlockChainQuery import *

"""
bubi区块链操作组件
author：mxd
"""
"""
1.1 获得密钥对
    ip
"""
def createAccount(ip):
    url = "http://" + ip + "/createAccount"
    param = ""
    return sendGet(url, param)
"""
1.2 获取nonce数值
    ip 
    sourceAddress
"""
def getnonce(ip,sourceAddress):
    nonce = -1
    res = getAccount1(ip,sourceAddress)
    if res['error_code'] ==0:
        print(res['error_code'])
        print(res['result'])
        if 'nonce' in res['result']:
            nonce = res['result']['nonce']
        else:
            nonce = 0
    return  nonce
"""
2.1 组件1：创建账号-操作码
    destAddress：新账号的地址
    initMetadata：账号初始储存信息
"""
def createAccountOper(destAddress,initMetadata):
    operation = {'type':1}
    #组装dest_address
    dest_address = {'dest_address': destAddress}
    #组装create_account1 dest_address
    create_account_value = {}
    create_account_value.update(dest_address)
    #组装metadatas
    metadatas_value = []
    value = {}
    if initMetadata:
        for e in initMetadata:
            val_key ={'key':e['key']}
            val_value = {'value':e['value']}
            value.update(val_key)
            value.update(val_value)
            metadatas_value.append(value)
    else:
        val_key = {'key': 'initMetadata'}
        val_value = {'value': 'create account'}
        value.update(val_key)
        value.update(val_value)
        metadatas_value.append(value)
    # 组装create_account2 metadatas
    metadatas = {'metadatas': metadatas_value}
    create_account_value.update(metadatas)
    # 组装priv
    priv_value = {}
    master_weight  = {'master_weight':10}
    signers ={'signers':[]}
    tx_threshold = {'thresholds': 7}
    thresholds_value ={}
    thresholds_value.update(tx_threshold)
    thresholds ={'thresholds':thresholds_value}
    priv_value.update(master_weight)
    priv_value.update(signers)
    priv_value.update(thresholds)
    priv ={'priv':priv_value}
    # 组装create_account3 priv
    create_account_value.update(priv)
    # 组装create_account
    create_account = {'create_account': create_account_value}
    operation.update(create_account)
    operations = operation
    # operations = json.dumps(operation,ensure_ascii=False)
    return operations
"""
2.2 组件2：发行资产-操作码
    destAddress：新账号的地址
    initMetadata：账号初始储存信息
"""
def issueAssetOper(amount,code):
    operation = {'type': 2}
    # 组装issue_asset_value
    issue_asset_value ={}
    amount ={'amount':amount}
    code ={'code':code}
    issue_asset_value.update(amount)
    issue_asset_value.update(code)
    # 组装issue_asset
    issue_asset = {'issue_asset': issue_asset_value}
    operation.update(issue_asset)
    operations = operation
    # operations = json.dumps(operation,ensure_ascii=False)
    return operations
"""
2.3 组件3：转移资产的操作码
    destAddress：新账号的地址
    issuer
    code
    amount
"""
def PaymentAssetOper(destAddress,sourceAddress,code,amount):
    operation = {'type': 3}
    # 组装payment_value
    payment_value ={}
    dest_address ={'dest_address':destAddress}
    payment_value.update(dest_address)
    #组装asset_value
    asset_value ={}
    property_value = {}
    issuer ={'issuer':sourceAddress}
    code = {'code':code}
    property_value.update(issuer)
    property_value.update(code)
    # 组装property
    property = {'property':property_value}
    amount ={'amount':amount}
    asset_value.update(property)
    asset_value.update(amount)
    asset = {'asset': asset_value}
    payment_value.update(asset)
    # 组装payment
    payment = {'payment': payment_value}
    operation.update(payment)
    operations = operation
    # operations = json.dumps(operation,ensure_ascii=False)
    return operations
"""
2.4 组件4：存储metadata的操作码
    key
    value
"""
def setMetadataOper(key,value):
    operation = {'type': 4}
    # 组装set_metadata_value
    set_metadata_value ={}
    key ={'key':key}
    value ={'value':value}
    set_metadata_value.update(key)
    set_metadata_value.update(value)
    # 组装set_metadata
    set_metadata = {'set_metadata': set_metadata_value}
    operation.update(set_metadata)
    operations = operation
    print(operations)
    # operations = json.dumps(operation,ensure_ascii=False)
    return operations
"""
交易1：序列化
    ip
    sourceAddress: 交易的发起方账号地址
    operations:序列化操作码
"""
def getTransactionBlob(ip,sourceAddress,operations):
    url ="http://"+ ip +"/getTransactionBlob"
    nonce = getnonce(ip,sourceAddress)+1
    if nonce==0:
        print("交易账号："+sourceAddress+"交易数nonce异常，交易中断！")
        return
    #组装transation
    transation = {}
    #组装source_address
    source_address = {'source_address':sourceAddress}
    transation.update(source_address)
    #组装nonce
    nonce = {'nonce':nonce}
    transation.update(nonce)
    #组装operations
    operations_value = [operations]
    operations = {'operations':operations_value}
    transation.update(operations)
    # data = json.dumps(transation, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    data = json.dumps(transation, ensure_ascii=False)
    data = eval(data)
    res = requests.post(url, json=data)
    return res.text
"""
交易2：签名
    privateKey:私钥
    blob:需要签名的16进制字符串blob
"""
def sign(privateKey,blob):
    # print(blob)
    url = "http://192.168.0.113:7706/sign"
    data = {'privateKey':privateKey,'blob':blob}
    data = json.dumps(data, ensure_ascii=False)
    data = eval(data)
    res = requests.post(url, json=data)
    return res.text
"""
交易3：组装提交交易数据
    ip
    sourceAddress
    operations
    privateKey
"""
def getsubmitValue(ip,sourceAddress,operations,privateKey):
    # 组装items_value
    items_value = {}
    #获取transaction_blob
    res_getTransactionBlob = json.loads(getTransactionBlob(ip,sourceAddress,operations))
    if res_getTransactionBlob:
        transaction_blob = res_getTransactionBlob['result']['transaction_blob']
        transaction_blob_value = transaction_blob
        transaction_blob = {'transaction_blob':transaction_blob}
        items_value.update(transaction_blob)
    else:
        print("transaction_blob为空，交易序列化失败，交易中断!")
        return

    # 交易签名
    res_sign = json.loads(sign(privateKey, transaction_blob_value))
    if res_sign:
        # 获取public_key
        public_key = res_sign['public_key']
        # 获取sign_data
        sign_data = res_sign['sign_data']
    else:
        print("用户签名为空，交易序列化失败，交易中断!")
        return
    # 组装signatures_value
    signatures_value  =[{'public_key':public_key,'sign_data':sign_data}]
    # 组装signatures
    signatures = {'signatures':signatures_value}
    items_value.update(signatures)
    items_value = [items_value]
    # 组装items
    items = {'items': items_value}
    return  items
"""
交易4：提交交易
    ip
    sourceAddress
    operations:   交易的操作内容
    privateKey
"""
def submitTransaction(ip,sourceAddress,operations,privateKey):
    items  = eval(json.dumps(getsubmitValue(ip,sourceAddress,operations,privateKey)))
    #提交交易
    url = "http://"+ ip +"/submitTransaction"
    res = requests.post(url, json=items)
    #查询交易
    res_text = res.json()
    print(res_text)
    res_transaction = res_text['results']
    print(res_transaction)
    transaction_hash = res_transaction[0]['hash']
    print(transaction_hash)
    # print(getTransactionHistory1(ip,transaction_hash))
    return res_text
if __name__ == '__main__':
    sourceAddress = "a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18"
    destAddress="a001dfd36749086b857d127ae3d66df81f5379c716e6d1"
    ip = "192.168.0.201:29334"
    initMetadata = [{
        "key": "测试",
        "value": "于2019.08.18 22：50分创建账号时设置的数据"
    }]
    transaction_hash = "536a38d3680bcdd53cc797ba705fa9cf980da970beaa7b094427075fed898aa8"
    print(getTransactionHistory1(ip, transaction_hash))
    # print(createAccountOper(destAddress,initMetadata))

