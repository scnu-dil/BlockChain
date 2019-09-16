import  pymysql
db=pymysql.connect(host="218.95..",port=61,user="lpf",passwd="jxsr****",db="dsj",charset="utf8")

# 连接数据库
cursor = cur = db.cursor()  # 获取数据库的游标

# 1、查询操作
cursor.execute('select * from person')  # 获取操作数据库的游标
results = cursor.fetchall()  # 获取查询结果  cursor.fetchone() 查询一条
for row in results:  # cursor.fetchmany(3)  查询前3条
    print(row)  # cursor.fetchall()   查询所有

# 2、插入操作
cursor.execute("insert into person values(1,'banana')")  # execute也可以执行创建和修改库与表语句
db.commit()
#提交

#  # 使用execute(sql, args) 方法
cursor.execute("insert into person values(%d,%s)", args=(1, 'banana'))
db.commit()
#提交

# 3、更新操作
cursor.execute("update person set name='jack' where id = 1")
db.commit()

# 4、删除操作
cur.execute("delete from person where id=1")

# 5、自动提交事务
db.autocommit(True)
#自动提交事务
