import sqlite3
import os
DB_FILE_PATH = 'E:/postgraduateLearning/web/projects/project_6/sqlite.db'
SHOW_SQL = True #是否打印sql
create_table_sql = "CREATE TABLE user(id integer primary key,username varchar(20) UNIQUE,password varchar(15) NOT NULL)"

query_sql = "select * from  user"


def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('path:'.format(path))
        return conn


def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()


def create_table(conn, sql):
    '''创建数据库表：user'''
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        if SHOW_SQL:
            print('执行sql:[{}]'.format(sql))
            try:
                cu.execute(sql)
                conn.commit()
                print('创建数据库表[user]成功!')
                close_all(conn, cu)
                return True
            except:
                print("Table user has existed ")
                return False
    else:
            print('the [{}] is empty or equal None!'.format(sql))
            return False


def drop_table(conn, table_name):
    '''如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！
    '''
    sql = 'DROP TABLE IF EXISTS ' + table_name
    if table_name is not None and table_name != '':
        if SHOW_SQL:
            print('执行sql:[{}]'.format(sql))
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('删除数据库表[{}]成功!'.format(table_name))
        close_all(conn, cu)
        return True
    else:
        print('the [{}] is empty or equal None!'.format(sql))
        return False


def close_all(conn, cu):
    '''关闭数据库游标对象和数据库连接对象'''
    try:
        if cu is not None:
            cu.close()
    finally:
        if cu is not None:
            cu.close()


def insert_data(conn, sql, data):
    '''插入数据'''
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            if SHOW_SQL:
                print('执行sql:[{}],参数:[{}]'.format(sql, data))
            cu.execute(sql,(data[0],data[1]))
            conn.commit()
            close_all(conn, cu)
            return True
    else:
        print('the [{}] is empty or equal None!'.format(sql))
        return False


def query_data(conn,sql):
    print("查询数据")
    cu = get_cursor(conn)
    cu.execute(sql)
    r = cu.fetchall()
    list_for_return = []
    if len(r) > 0:
        for e in r:
            users = e
            list_for_return.append(users)
    return list_for_return