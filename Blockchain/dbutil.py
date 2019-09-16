import  pymysql
from Blockchain.BlockChainTransaction import *
import openpyxl

"""
数据库的操作
"""
db=pymysql.connect(host="120.79.169.95",port=3306,user="root",passwd="root",db="SchoolBlockchain",charset="utf8")
# 连接数据库
cursor = cur = db.cursor()  # 获取数据库的游标

# 1、查询学号对应的区块链账号及密钥信息
def getuserAccountinfo(userid):
    userAccountinfo = {}
    sql = "select b.account,b.private_key,b.public_key from user u,BubiAccount b WHERE u.account = b.account AND u.user_id = "+userid
    print(sql)
    cursor.execute(sql)  # 获取操作数据库的游标
    results = cursor.fetchone()  # 获取查询结果  cursor.fetchone() 查询一条
    print(results)
    account = {'account':results[0]}
    private_key = {'private_key':results[1]}
    public_key = {'public_key': results[2]}
    userAccountinfo.update(account)
    userAccountinfo.update(private_key)
    userAccountinfo.update(public_key)
    return userAccountinfo
#2、查询学生是否存在
def getUser(userid):
    sql = "select * from user  WHERE user_id = "+userid
    cursor.execute(sql)  # 获取操作数据库的游标
    results = cursor.fetchone()  # 获取查询结果  cursor.fetchone() 查询一条 cursor.fetchall() 查询多条
    return results
#3、添加学生
def addUser(userinfo,info):
    #先创建区块链账号，得到destAddress
    destAddress = FcreateAccount(info['ip'],info['sourceAddress'],info['initMetadata'],info['privateKey'])
    addBubi(destAddress)
    if destAddress:

        sql = "insert into user values('20172131104','林茂森','2019Spring','a00126ff34e8492cf12644f93fd62e1401a8eb1ea6f622',0,0)"#sql = "insert into user values('"+userinfo['user_id']+"','"+userinfo['user_name']+"','"+userinfo['class_name']+"','"+destAddress['address']+"','0','0')"
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("添加学生成功！")
    else:
        print("添加学生失败！")
#4、更新用户积分
#   amount
#   code

"""
#获取交易传参info

"""
def updateUser(userid,account,f_points,r_points):
    print(userid)
    print(account)
    print(f_points)
    print(r_points)
    sql = str("update user set account = '"+str(account)+"',f_points ='"+str(f_points)+"', r_points = '"+str(r_points)+"' where user_id = "+str(userid))
    print(sql)
    cursor.execute(sql)
    db.commit()


#5、添加用户区块链账号
#   amount
#   code
def addBubi(Accountinfo):
    address = Accountinfo['address']
    private_key = Accountinfo['private_key']
    private_key_aes = Accountinfo['private_key_aes']
    public_key = Accountinfo['public_key']
    public_key_raw = Accountinfo['public_key_raw']
    sign_type = Accountinfo['sign_type']
    sql = "insert into BubiAccount VALUES(0,'"+address+"','"+private_key+"','"+private_key_aes+"','"+public_key+"','"+public_key_raw+"','"+sign_type+"')"
    cursor.execute(sql)
    db.commit()

if __name__ == '__main__':
    accountinfo = {'address': 'a001a1166a0c8be7655531e25de629f135bf6c53435599', 'private_key': 'c001967c5f11a5faa715c658a8cccdf359633f9ccc390c47d0714595250a827f6c646a', 'private_key_aes': '4ee78aa30b2b8e1da0489cdbbefe708d7248fa658189ec4992fbdb7e6708de5f7919113eec325543e121575bb69ab758a03f5b76c78cf4d4d45038a34552d6dbafbe638ffd2b5dd53c4f098fd466ae56', 'public_key': 'b00133a699909222b53a9637e47c501fe40943e4456f443ac90706289165f9f62c3fca', 'public_key_raw': '33a699909222b53a9637e47c501fe40943e4456f443ac90706289165f9f62c3f', 'sign_type': 'ed25519'}
    addBubi(accountinfo)
    # userid = "11"
    # getuserAccountinfo(userid)
    # getUser(userid)

