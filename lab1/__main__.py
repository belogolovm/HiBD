import os
import sys

from lab1.migration import migrate_all
from .model import init_sql_engines, init_mongo_engine, check_connection, databases

if __name__ == '__main__':
    # Костыль для поддержки UTF-8 в Oracle
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'

    init_sql_engines()
    init_mongo_engine()

    check_connection()

    if sys.argv[1] == 'create':

        from lab1.model.postgres import create_schema as postgres_create_schema
        from .generator.postgres import fill_postgres
        postgres_create_schema(databases['postgres']['engine'])
        fill_postgres()

        from lab1.model.mysql import create_schema as mysql_create_schema
        from .generator.mysql import fill_mysql
        mysql_create_schema(databases['mysql']['engine'])
        fill_mysql()

        from lab1.model.oracle import create_schema as oracle_create_schema
        from .generator.oracle import fill_oracle
        oracle_create_schema(databases['oracle']['engine'])
        fill_oracle()

        from .generator.mongo import fill_mongo
        fill_mongo()

    elif sys.argv[1] == 'migrate':

        from .model.final import drop_schema as final_drop_schema, create_schema as final_create_schema
        final_drop_schema(databases['oracle']['engine'])
        final_create_schema(databases['oracle']['engine'])

        migrate_all()


    else:

        print('Неизвестный ключ')
        exit(1)