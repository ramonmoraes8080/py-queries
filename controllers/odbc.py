import json
import pyodbc
# from models.connections import Connection


class ODBCConnection(object):

    def __init__(self, name):
        conn = self.get_connection_details_by_name(name)
        self.server = conn.get('host')
        self.database = conn.get('database')
        self.uid = conn.get('user')
        self.pwd = conn.get('pswd')

    def get_connection_details_by_name(self, name):
        with open('connections.json', 'r') as f:
            return json.loads(f.read() or '{}')[name]

    def connect(self):
        self.cnxn = pyodbc.connect(
            f'DRIVER={self.driver_name};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.uid};'
            f'PWD={self.pwd}'
            )
        return self.cnxn

    def query(self, sql_query):
        cur = self.cnxn.cursor()
        rows = cur.execute(sql_query).fetchall()
        #import pdb; pdb.set_trace()
        return cur.description, rows

    def close(self):
        self.cnxn.close()


class ODBCPostgresql(ODBCConnection):

    driver_name = 'psqlodbc'

    def connect(self):
        cnxn = super().connect()
        # Python 3.x
        cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        cnxn.setencoding(encoding='utf-8')
        return cnxn


class ODBCSQLite(ODBCConnection):

    driver_name = 'SQLite'

    def get_conn_str(self):
        ret = (
            f'DRIVER={self.driver_name};'
            f'DATABASE={self.server};'
        )
        print(ret)
        return ret

    def connect(self):
        # Specifying the ODBC driver, server name, database, etc. directly
        self.cnxn = pyodbc.connect(self.get_conn_str())
        self.cnxn.autocommit = True
        return self.cnxn

