import functools
import time

from django.db import connection, reset_queries

from .loggers import log

def query_debugger(*, verbose=False, cut_lines=False):
    """ Декоратор для оценки SQL запросов декорируемой функции
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            reset_queries()

            start_queries = len(connection.queries)

            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            end_queries = len(connection.queries)

            if verbose:
                for query in connection.queries:
                    query_sql, query_time = query['sql'], query['time']
                    log.info(
                        f"sql: {query_sql[:100] if cut_lines else query_sql} time: {query_time}"
                    )

            log.info(f"Function : {func.__name__}")
            log.info(f"Number of Queries : {end_queries - start_queries}")
            log.info(f"Finished in : {(end - start):.2f}s")
            return result
        return wrapper
    return decorator
