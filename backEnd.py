from sqlalchemy import create_engine
from urllib.parse import quote_plus

class BackEnd:
    def connect_db(self, user, pwd, server):
        user = quote_plus(user)
        pwd = quote_plus(pwd)
        server = quote_plus(server)
        db = quote_plus('Vista_Replication_PRD')
        try:
            engine = create_engine(f"mssql+pyodbc://{user}:{pwd}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
            self.conn = engine.connect()
            return 'Conectado'
        except Exception as erro: 
            return str(erro)