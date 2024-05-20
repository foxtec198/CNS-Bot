from sqlalchemy import create_engine
from urllib.parse import quote_plus

class BackEnd:
    def connect_db(self, uid, pwd, server, database='Vista_Replication_PRD', driver='ODBC Driver 17 for SQL Server'):
        self.uid = quote_plus(uid)
        self.pwd = quote_plus(pwd)
        self.server = quote_plus(server)
        self.database = quote_plus(database)
        driver = quote_plus(driver)
        url = f'mssql://{self.uid}:{self.pwd}@{self.server}/{self.database}?driver={driver}'
        try:
            engine = create_engine(url)
            self.conn = engine.connect()
            return 'Conectado'
        except Exception as erro: 
            return str(erro)