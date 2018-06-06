import threading
import traceback
from pymssql import connect
from pymssql import Connection


class Pool(object):
    def __init__(self, host, port, user, pswd, database, **argvs):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__pswd = pswd
        self.__database = database

        if 'timeout' in argvs:
            self.__timeout = argvs['timeout']
        else:
            self.__timeout = 60

        if 'login_timeout' in argvs:
            self.__login_timeout = argvs['login_timeout']
        else:
            self.__login_timeout = 60

        self.__autocommit = True

        if 'max' in argvs:
            self.__max = argvs['max']
        else:
            self.__max = 10

        self.__pool = []
        self.__lock = threading.Lock()

    def acquire(self):
        self.__lock.acquire()
        try:
            if self.__pool:
                conn = self.__pool.pop()
                if self.__valid(conn):
                    return conn
                conn.close()
            return self.__open()
        finally:
            self.__lock.release()

    def __open(self):
        return connect(host=self.__host,
                       port=self.__port,
                       user=self.__user,
                       password=self.__pswd,
                       database=self.__database,
                       timeout=self.__timeout,
                       login_timeout=self.__login_timeout,
                       as_dict=True,
                       autocommit=self.__autocommit)

    @staticmethod
    def __valid(conn):
        try:
            curs = conn.cursor()
            curs.execute('select 0 as status')
            curs.fetchone()
            return True
        except:
            traceback.print_exc()
            return False
        finally:
            if curs is not None:
                curs.close()

    def release(self, conn):
        if isinstance(conn, Connection):
            self.__lock.acquire()
            try:
                if len(self.__pool) >= self.__max:
                    conn.close()
                else:
                    conn.autocommit(self.__autocommit)
                    self.__pool.append(conn)
            finally:
                self.__lock.release()
