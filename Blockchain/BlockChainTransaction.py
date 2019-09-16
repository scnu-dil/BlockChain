from Blockchain.BlockChainUtil import *

"""
bubi区块链交易工具
author：mxd
"""
"""
1 创建账号
    ip
    sourceAddress: 发起创建账号交易的账号地址
    initMetadata: 创建账号时储存的初始信息
    privateKey：发起创建账号交易的账号私钥
"""
def FcreateAccount(ip,sourceAddress,initMetadata,privateKey):
    #获取密钥对
    res_createAccount = createAccount(ip)['result']

    destAddress = res_createAccount['address']
    if destAddress:
        operations = createAccountOper(destAddress,initMetadata)
        submitTransaction(ip,sourceAddress,operations,privateKey)
    else:
        print("账号不存在，交易失败！")
        return
    return res_createAccount
"""
2 发行资产
    ip
	sourceAddress
	privateKey
	code
	amount
"""
def Fissue(ip,sourceAddress,privateKey,code,amount):
    operations = issueAssetOper(amount,code)
    submitTransaction(ip,sourceAddress,operations,privateKey)

"""
3 转移资产
    ip
	sourceAddress：支付方地址
	destAddress:收款方地址
	privateKey：支付方密钥
	issuerAddress：资产发行方地址
	code：资产代码
	amount：数量
"""
def Fpay(ip,sourceAddress,destAddress,privateKey,issuerAddress,code,amount):
    operations  = PaymentAssetOper(destAddress,issuerAddress,code,amount)
    submitTransaction(ip,sourceAddress,operations,privateKey)
"""
4 set_metadata
    ip
	sourceAddress：支付方地址
	destAddress:收款方地址
	privateKey：支付方密钥
	issuerAddress：资产发行方地址
"""
def Fset_metadata(ip,sourceAddress,privateKey,key,value):
    operations = setMetadataOper(key,value)
    submitTransaction(ip,sourceAddress,operations,privateKey)

if __name__ == '__main__':
    """设置数据的参数格式"""
    ip = "192.168.0.201:29334"
    sourceAddress = "a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18"
    key = "2019-06-03 21:57:40"
    value = "login"
    privateKey = 'c00205ce8de2892b26c3b95caf3404831d6e913c655d85b517f076380ebfcbef47ff8f'
    nnum = Fset_metadata(ip, sourceAddress, privateKey, key, value)
    print(nnum)

