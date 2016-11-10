from flask import Flask,request, render_template, url_for, redirect, make_response, session
from DatabaseOperation import *
import re
import json
import psutil
from functools import wraps

app = Flask(__name__)
DB_FILE_PATH = 'sqlite.db'
create_table_sql = "CREATE TABLE user(username varchar(20) UNIQUE,password varchar(15) NOT NULL)"
insert_sql = "INSERT INTO user values(?,?)"
query_sql = "SELECT username from user"
conn = get_conn(DB_FILE_PATH)
create_table(conn, create_table_sql)

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


@app.route("/", methods=['POST','GET'])
@allow_cross_domain
def index():
    print("index")
    if request.method == 'POST':
        print("POST")
        mem = psutil.virtual_memory()
        mem_str = ""
        mem_str = mem_str + str(mem.used/mem.total)
        mem_str = mem_str + ";" + str(psutil.cpu_percent())
        print(mem_str)
        return mem_str
    else:
        return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
@allow_cross_domain
def register():
    """检查邮箱是否合法，检查两次密码是否一致"""
    print("register")
    if request.method == 'POST':
        print("post")
        data = json.loads(request.form.get("data"))
        username = data["username"]
        password = data["password"]

        print("register:" + username+" "+password)
        user_list = query_data(conn, query_sql)
        user_name_list =[]

        for user in user_list:
            user_name_list.append(user[0])
        print("user_name_list:", user_name_list)
        if username not in user_name_list:
            data = [username, password]
            insert_data(conn, insert_sql, data)
            print('注册成功')
            return "success"
        else:
            print("用户名已存在")
            return "failed"
    else:
        print("get方法请求register")
        return render_template("register.html")


def isUser(username, password):
    conn = get_conn('sqlite.db')
    data_user = query_data(conn, "SELECT * from user")
    print(data_user)
    for i in data_user:
        print(i)
        if (username==i[0]):
            return i
    return "Username not exist"


@app.route("/login", methods=['GET', 'POST'])
@allow_cross_domain
def login():
    print("进入login")
    if request.method == 'POST':
        print("post")
        data = json.loads(request.form.get("data"));
        username = data["username"]
        password = data["password"]
        print("login:" + username + "--password: " + password)
        result = isUser(username, password)
        print("login result:" + json.dumps(result))
        return json.dumps(result)
    else:
        print("unpost")
        return render_template('login.html')


def validate_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return True
    return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)