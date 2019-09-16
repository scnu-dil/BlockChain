from  Blockchain.dbutil import *
from Blockchain.BlockChainTransaction import *
#获取个人登录信息
def  getLogininfo(user_id,start_time,end_time):
    #用户行为:登录
    #发送http请求 获取学者网的单个用户登录行为数据
    url= "http://www.scholat.com/rest/courseOapi/loginInfo/14da67741f1ae95eb1f8e0795aeb8152/2/"+user_id+"/"+start_time+"/"+end_time
    param = ""
    res = sendGet(url, param)
    print(res)
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
    #res = json.loads('{"stuid":"20172131061","type":"question","content":{"2019-06-03 21:57:03":"关于代码修改###<p>老师您好，我发现最新的那个RNN的代码同样的参数，随着参数初始化的不同导致TESTLOSS有的时候很高，有时候很低，那我应该把哪个TESTLOSS截图上交呢。比如同样的参数有时候是这个<img src=\\"/resources/p_picture/xielidong_1559570090003.png\\"/>，有时候是这个<img src=\\"/resources/p_picture/xielidong_1559570209691.png\\"/></p>"}}')
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
    if logininfo['content']:
        userbehaviour.append(logininfo)
    questinfo = getQuestinfo(userinfo['user_id'], time['start_time'], time['end_time'])
    if questinfo['content']:
        userbehaviour.append(questinfo)
        print(userbehaviour)
    answerinfo = getAnswerinfo(userinfo['user_id'], time['start_time'], time['end_time'])
    if answerinfo['content']:
        userbehaviour.append(answerinfo)
    if userbehaviour:
        return userbehaviour
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
    info = {"ip": "192.168.0.201:29334","sourceAddress":"a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18","issuerAddress" :"a0025e6de5a793da4b5b00715b7774916c06e9a72b7c18","initMetadata":[{"key": "add_address", "value": "于2019.08.20 0：20分创建账号时设置的数据"}],"privateKey" :"c00205ce8de2892b26c3b95caf3404831d6e913c655d85b517f076380ebfcbef47ff8f"}
    time_list = {"start_time":"2019-01-01","end_time":"2019-09-01"}
    # 调用各接口完成积分分发
    userinfo = {'class_name': '2019Spring', 'user_id': '20172131104', 'user_name': '林茂森'}
    print(userinfo)

    # """判断数据库中是否存在该用户id及区块链账号"""
    # res_sql_user = getUser(userinfo['user_id'])
    # print(res_sql_user)
    # if res_sql_user:
    #     if getUser(res_sql_user['account']):
    #         print("该学生账号及区块链账号均已经存在!")
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
    #     print(userinfo)
    #     print(info)
    #     #数据库中没有该用户存在，则创建用户及区块链账号
    # addUser(userinfo, info)
        #完成了数据库中用户及区块链账号的创建

    """获取新创建的账号信息，方便进行setmatedata"""
    account_info = getuserAccountinfo(userinfo['user_id'])
    print(account_info)

    """获取用户行为,为区块链分发积分和区块链存储行为做准备"""
    res_behaviour = getUserBehaviour(userinfo,time_list)
    print(res_behaviour)
    #res_behaviour =[{"stuid": "20172131061", "type": "login", "content": {"2019-06-03 21:57:03", "2019-06-03 21:57:40"}},{"stuid":"20172131061","type":"question","content":{"2019-06-03 21:57:03":"##########","2019-06-03 21:57:40":"**********"}}]
    #行为兑积分规则
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
                    Fset_metadata(info['ip'],account_info['account'],account_info['private_key'],key_value,i['type'])
                    #根据登录次数获得积分
                    amount = get_num(data)
                    r = Fpay(info['ip'], info['sourceAddress'],account_info['account'],info['privateKey'],info['issuerAddress'],code,amount)
                    if r:
                            #区块链上成功发放积分后，更新数据库表中的固定积分分值
                            #1：查询固定积分
                            r_points = getUser(userinfo['user_id'])[5]+amount
                            updateUser(userinfo['user_id'],account_info['account'],getUser(userinfo['user_id'])[4],r_points)
            elif "question" == i['type']:
                        code = "活动积分"
                        data = i['content']
                        #向区块链本账户地址写入content内容
                        for d in data:
                            print(d)
                            key_value = d
                            Fset_metadata(info['ip'], account_info['account'], account_info['private_key'],key_value,i['type'])
                        #根据登录次数获得积分
                        amount = get_num(data)
                        Fpay(info['ip'], info['sourceAddress'], account_info['account'], info['privateKey'],info['issuerAddress'], code, amount)
                        # 区块链上成功发放积分后，更新数据库表中的活动积分分值
                        # 1：查询活动积分
                        f_points = getUser(userinfo['user_id'])[4] + amount
                        updateUser(userinfo['user_id'], account_info['account'], f_points, getUser(userinfo['user_id'])[5])
            elif "answer" == i['type']:
                        code = "活动积分"
                        data = i['content']
                        # 向区块链本账户地址写入content内容
                        for d in data:
                            key_value = d
                            Fset_metadata(info['ip'], account_info['account'], account_info['private_key'],
                                          key_value, i['type'])
                        #根据登录次数获得积分
                        amount = get_num(data)
                        r = Fpay(info['ip'], info['sourceAddress'], account_info['account'], info['privateKey'],info['issuerAddress'], code, amount)
                        if r:
                            # 区块链上成功发放积分后，更新数据库表中的活动积分分值
                            # 1：查询活动积分
                            f_points = getUser(userinfo['user_id'])[4] + amount
                            updateUser(userinfo['user_id'], account_info['account'], f_points, getUser(userinfo['user_id'])[5])
            print("成功！")





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
