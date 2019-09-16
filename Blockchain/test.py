import json

# txt = json.loads('{"stuid":"20172131061","type":"question","content":{"2019-06-03 21:57:03":"关于代码修改###<p>老师您好，我发现最新的那个RNN的代码同样的参数，随着参数初始化的不同导致TESTLOSS有的时候很高，有时候很低，那我应该把哪个TESTLOSS截图上交呢。比如同样的参数有时候是这个<img src=\\"/resources/p_picture/xielidong_1559570090003.png\\"/>，有时候是这个<img src=\\"/resources/p_picture/xielidong_1559570209691.png\\"/></p>"}}')
# print(txt)
userid = 89289
account = 234
f_points =21
r_points = 0

sql = "update user set account = '"+str(account)+"',f_points ='"+str(f_points)+"', r_points = '"+str(r_points)+"' where user_id = "+str(userid)
print(sql)



