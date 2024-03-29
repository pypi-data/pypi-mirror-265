from . import sql_support
# Don't remove. Import for not repetitive implementation
from sqlexec import insert, save, save_select_key, batch_insert, batch_execute, do_execute, do_save_sql, do_save_sql_select_key, do_get, do_query,\
    do_query_one, do_select,do_select_one, do_select_page, do_query_page, do_select_page, do_query_page, load, do_load, insert_from_csv,\
    insert_from_df, insert_from_json, truncate, drop, table


def save_sql(sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.save_sql', sql, *args, **kwargs)
    return do_save_sql(sql, *args)


def save_sql_select_key(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.save_sql', sql, *args, **kwargs)
    return do_save_sql_select_key(select_key, sql, *args)


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.execute', sql, *args, **kwargs)
    return do_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.get', sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.query', sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.query_one', sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.select', sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.select_one', sql, *args, **kwargs)
    return do_select_one(sql, *args)


# ----------------------------------------------------------Page function------------------------------------------------------------------
def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_page_mapping('query_page', sql, page_num, page_size, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_page_mapping('select_page', sql, page_num, page_size, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


from .sql_page_exec import sql, page
