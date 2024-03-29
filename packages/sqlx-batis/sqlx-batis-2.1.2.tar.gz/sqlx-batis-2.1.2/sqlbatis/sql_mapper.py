import os
import sqlexec
import functools
from .log_support import logger
from .support import SqlAction, DBError
from .sql_support import simple_sql, get_named_sql_args
from .sql_holder import get_sql_model, do_get_sql, build_sql_id

_UPDATE_ACTIONS = (SqlAction.INSERT.value, SqlAction.UPDATE.value, SqlAction.DELETE.value, SqlAction.CALL.value)


def mapper(namespace: str = None, sql_id: str = None, batch=False, return_key=False, select_key=None):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            param_names = func.__code__.co_varnames
            full_sql_id, func_name = before(func, namespace, sql_id, *args, **kwargs)
            sql_model = get_sql_model(full_sql_id)
            exec_func = get_exec_func(func, sql_model.action, batch)
            if return_key:
                use_select_key = select_key
                use_sql, args = do_get_sql(sql_model, batch, param_names, *args, **kwargs)
                if use_select_key is None:
                    use_select_key = sql_model.select_key
                    if use_select_key is None:
                        try:
                            use_select_key = sqlexec.Dialect.get_select_key(sql=use_sql)
                        except NotImplementedError:
                            return DBError(
                                f"Expect 'select_key' but not. you can set it in mapper file with 'selectKey', or @mapper with 'select_key'")
                return sqlexec.do_save_sql_select_key(use_select_key, use_sql, *args)
            if batch:
                if kwargs:
                    logger.warning("Batch exec sql better use like '{}(args)' or '{}(*args)' then '{}(args=args)'".format(func_name, func_name, func_name))
                    args = list(kwargs.values())[0]
                use_sql, _ = do_get_sql(sql_model, batch, param_names, *args)
            else:
                use_sql, args = do_get_sql(sql_model, batch, param_names, *args, **kwargs)
            return exec_func(use_sql, *args)

        return _wrapper

    return _decorator


def sql(value: str, batch=False, return_key=False, select_key=None):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_sql = value
            low_sql = value.lower()
            if any([action in low_sql for action in _UPDATE_ACTIONS]):
                if batch:
                    if kwargs:
                        args = list(kwargs.values())[0]
                    return sqlexec.batch_execute(use_sql, *args)
                if return_key:
                    use_select_key = select_key
                    if use_select_key is None:
                        try:
                            use_select_key = sqlexec.Dialect.get_select_key(sql=use_sql)
                        except NotImplementedError:
                            return DBError(f"Expect 'select_key' but not in func '{func.__name__}' at file: '{func.__code__.co_filename}', line {func.__code__.co_firstlineno}. you can set it @sql with 'select_key'")
                    assert SqlAction.INSERT.value in low_sql, 'Only insert sql can return primary key.'
                    if kwargs:
                        use_sql, args = get_named_sql_args(use_sql, **kwargs)
                    return sqlexec.do_save_sql_select_key(use_select_key, use_sql, *args)

                if kwargs:
                    use_sql, args = get_named_sql_args(use_sql, **kwargs)
                return sqlexec.do_execute(use_sql, *args)
            elif SqlAction.SELECT.value in low_sql:
                select_func = get_select_func(func)
                use_sql, args = simple_sql(use_sql, *args, **kwargs)
                return select_func(use_sql, *args)
            else:
                return ValueError("Invalid sql: {}.".format(sql))

        return _wrapper

    return _decorator


def get_exec_func(func, action, batch):
    if action == SqlAction.SELECT.value:
        return get_select_func(func)
    elif batch:
        return sqlexec.batch_execute
    else:
        return sqlexec.do_execute


def get_select_func(func):
    names = func.__code__.co_names
    is_list = 'list' in names or 'List' in names
    if 'Mapping' in names and is_list:
        return sqlexec.do_query
    elif 'Mapping' in names:
        return sqlexec.do_query_one
    elif len(names) == 1 and names[0] in ('int', 'float', 'Decimal', 'str', 'AnyStr', 'date', 'time', 'datetime'):
        return sqlexec.do_get
    elif len(names) == 1 and names[0] in ('tuple', 'Tuple'):
        return sqlexec.do_select_one
    elif is_list:
        return sqlexec.do_select
    else:
        return sqlexec.do_query


def before(func, namespace, _id, *args, **kwargs):
    file_name = os.path.basename(func.__code__.co_filename)[:-3]
    _namespace = namespace if namespace else file_name
    _id = _id if _id else func.__name__
    sql_id = build_sql_id(_namespace, _id)
    func_name = file_name + '.' + func.__name__
    logger.debug("Exec mapper func: '%s', sql_id: '%s', args: %s, kwargs: %s" % (func_name, sql_id, args, kwargs))
    return sql_id, func_name
