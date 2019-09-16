from  Blockchain.dbutil import *
from Blockchain.BlockChainTransaction import *
#获取个人登录信息
def  getLogininfo(user_id,start_time,end_time):
    #用户行为:登录
    #发送http请求 获取学者网的单个用户登录行为数据
    url= "http://www.scholat.com/rest/courseOapi/loginInfo/14da67741f1ae95eb1f8e0795aeb8152/2/"+user_id+"/"+start_time+"/"+end_time
    param = ""
    res = sendGet(url, param)
    #得到用户登录的信息
    """
   {'stuid': '20172131123',
    'type': 'login',
     'list': {'2019-07-22 10:37:07', '2019-07-26 09:31:50', '2019-08-09 13:19:37', '2019-08-10 21:17:45'}
     }
    """
    return res
#获取个人提问信息
def  getQuestinfo(user_id,start_time,end_time):
    #用户行为:提问
    #发送http请求 获取学者网的单个用户提问行为数据
    url= "http://www.scholat.com/rest/courseOapi/questionInfo/14da67741f1ae95eb1f8e0795aeb8152/2/"+user_id+"/"+start_time+"/"+end_time
    param = ""
    res = sendGet(url, param)
    #得到用户提问的信息
    """
   {'stuid': '20172131010',
    'type': 'question', 
    'list': []}
    """
    return res
#获取个人回答信息
def  getAnswerinfo(user_id,start_time,end_time):
    #用户行为:回复
    #发送http请求 获取学者网的单个用户回复行为数据
    url= "http://www.scholat.com/rest/courseOapi/answerInfo/14da67741f1ae95eb1f8e0795aeb8152/2/"+user_id+"/"+start_time+"/"+end_time
    param = ""
    res = sendGet(url, param)
    #得到用户回复的信息
    """
   {'stuid': '20172131010',
    'type': 'question', 
    'list': []}
    """
    return res

def getUserBehaviour(userinfo,time):
    userbehaviour = []
    logininfo = getLogininfo(userinfo['user_id'],time['start_time'],time['end_time'])
    if logininfo['list']:
        userbehaviour.append(logininfo)
    questinfo = getQuestinfo(userinfo['user_id'], time['start_time'], time['end_time'])
    if questinfo['list']:
        userbehaviour.append(logininfo)
    answerinfo = getAnswerinfo(userinfo['user_id'], time['start_time'], time['end_time'])
    if answerinfo['list']:
        userbehaviour.append(logininfo)
    if userbehaviour:
        print(userbehaviour)
    else:
        return
def get_num(data):
    num = 0
    for e in data:
        num = num+1
    return  num
#执行交易
def pay_points():
    pass


if __name__ == '__main__':
    info = {
        "ip": "192.168.0.201:29334",
        "sourceAddress ":"a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18",
        "issuerAddress" : "a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18",
        "privateKey" :"c00205ce8de2892b26c3b95caf3404831d6e913c655d85b517f076380ebfcbef47ff8f"
    }
    time_list = {"start_time":"2019-01-01","end_time":"2019-09-01"}

    # 调用各接口完成积分分发
    """
    流程介绍
    1：读取课程用户信息表存入user.txt中
    2：循环读取user.txt的元素，得到单个学生的信息userinfo
    3：通过getUser(userinfo['user_id'])来查询学生在本地数据库user表是否存在，
        如果没有存在，addUser(userinfo)
        如果存在了，获取返回结果的user_id，查询有没有区块链账号，getuserAccountinfo(user_id)
            如果区块链账号没有存在，创建区块链账号：FcreateAccount(ip, sourceAddress, initMetadata, privateKey)
            如果区块链账号存在，不做任何操作
    """
    with open('./user.txt','r',encoding='utf8') as f:
        data = json.load(f)
        for e in data:
            userinfo = e
            print(getUser('1'))
            #根据user_id，查看数据库是否有该用户存在
            #res_sql_user = getUser(userinfo['user_id'])
            # if res_sql_user:
            #     if getUser(userinfo['account']):
            #         print("该学生账号及区块链账号均已经存在。")
            #         continue
            #     else:
            #         destAddress = FcreateAccount(info['ip'], info['sourceAddress'], info['initMetadata'],info['privateKey'])
            #         #成功了创建一个区块链账号
            #         if destAddress:
            #             #更新账号到数据库中
            #             updateUser(userinfo['user_id'], destAddress, 0, 0)
            #             print("已为该用户创建区块链账号！")
            #         else:
            #             print("为该用户创建区块链账号失败！")
            # else:
            #     #数据库中没有该用户存在，则创建用户及区块链账号
            #     addUser(userinfo, info)
            # #完成了数据库中用户及区块链账号的创建
            # #获取新创建的账号信息，方便进行setmatedata
            #account_info = getuserAccountinfo(userinfo['user_id'])
            #获取该用户行为
            res_behaviour = getUserBehaviour(userinfo,time_list)
            res_behaviour =[{"stuid": "20172131061", "type": "login", "content": {"2019-06-03 21:57:03", "2019-06-03 21:57:40"}},{"stuid":"20172131061","type":"question","content":{"2019-06-03 21:57:03":"##########","2019-06-03 21:57:40":"**********"}}]

            if res_behaviour:
                for i in res_behaviour:
                    print(i)
                    #1：根据不同行为设置code和amount
                    if "login" == i['type']:
                        code = "固定积分"
                        data = i['content']
                        # 向区块链本账户地址写入content内容
                        for d in data:
                            key_value = d
                            Fset_metadata(info['ip'],account_info['destAddress'],account_info['privateKey'],key_value,i['type'])
                        #根据登录次数获得积分
                        amount = get_num(data)
                        r = Fpay(info['ip'], info['sourceAddress'],account_info['destAddress'],info['privateKey'],info['issuerAddress'],code,amount)
                        if r:
                            #区块链上成功发放积分后，更新数据库表中的固定积分分值
                            #1：查询固定积分
                            r_points = res_sql_user[5]+amount
                            updateUser(userinfo['user_id'],account_info['destAddress'],res_sql_user[4],r_points)
                    elif "question" == i['type']:
                        code = "活动积分"
                        data = i['content']

                        #向区块链本账户地址写入content内容

                        #根据登录次数获得积分
                        amount = get_num(data)
                        r = Fpay(info['ip'], info['sourceAddress'], account_info['destAddress'], info['privateKey'],
                                 info['issuerAddress'], code, amount)
                        if r:
                            # 区块链上成功发放积分后，更新数据库表中的活动积分分值
                            # 1：查询活动积分
                            f_points = res_sql_user[4] + amount
                            updateUser(userinfo['user_id'], account_info['destAddress'], f_points, res_sql_user[5])
                    elif "answer" == i['type']:
                        code = "活动积分"
                        data = i['content']

                        # 向区块链本账户地址写入content内容

                        #根据登录次数获得积分
                        amount = get_num(data)
                        r = Fpay(info['ip'], info['sourceAddress'], account_info['destAddress'], info['privateKey'],info['issuerAddress'], code, amount)
                        if r:
                            # 区块链上成功发放积分后，更新数据库表中的活动积分分值
                            # 1：查询活动积分
                            f_points = res_sql_user[4] + amount
                            updateUser(userinfo['user_id'], account_info['destAddress'], f_points, res_sql_user[5])






    """

    4：以上三步已经完成数据库中user信息与区块链账号信息的绑定
        根据user_id获取到区块链账号地址：getuserAccountinfo(userid)
        返回值是：account、private_key、public_key
    5: 根据用户id获取用户行为
        1）getLogininfo
        2）getQuestinfo
        3）getAnswerinfo
        根据list的记录数发积分给用户账号，同时更新数据库用户积分，并在该用户账号下setmatedata，记录用户行为。
        行为对应的交易金额与交易代码
        用户行为：
            1：登录：code = r_points，amount = 1
            2：提问：code =f_points，amount= 1
            3：回复：code= f_points，amount= 1
    """
