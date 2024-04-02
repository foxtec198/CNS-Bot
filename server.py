import telebot
import msgP
from sqlalchemy import create_engine
from pandas import read_sql_query
from dataframe_image import export
from time import strftime as st
from os import system
from urllib import parse

API  = '7134052176:AAHfgBxarhx3wj5N8sTtFNRawuWt3PaXv0k'
bot = telebot.TeleBot(API)

# Conectar
class CNS:
    def Conn(self, msg, user, pwd, server='10.56.6.56', db='Vista_Replication_PRD'):
        user = parse.quote_plus(user)
        pwd = parse.quote_plus(pwd)
        try:
            self.engine = create_engine(f"mssql+pyodbc://{user}:{pwd}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes")
            self.conn = self.engine.connect()
            bot.reply_to(msg, 'Conexão Ativa 🟢')
            return True
        except Exception as error:
            bot.reply_to(msg, f"""Conexão Inválida 🔴: \n Erro: {error}""")
            return False

    def consultar(self, msg, tipo=None):
        now = st('%x - %X')
        day = st('%d')
        month =st('%m')
        year = st('%Y')

        c = self.Conn(msg, 'guilherme.breve','84584608@Gui')

        if c:
            valor = msg.text.split()
            print(valor)
            try:
                match len(valor):
                    case 1: 
                        if tipo < 3: bot.reply_to(msg, 'Digite o CR antes de Consultar!')
                        if tipo >= 3 and tipo <= 4: bot.reply_to(msg, 'Digite a GERENCIA antes de Consultar!')
                    case 2:
                        if tipo < 3: Att = ''
                        if tipo >= 3: Att = valor[1]
                    case 3: 
                        if tipo < 3: Att = valor[2]
                        if tipo >= 3: Att = valor[1]

                match valor[0]:
                    case '/gerente': Gerente = Att.replace('_', ' ')
                    case '/gerentem': Gerente = Att.replace('_', ' ')
                    case '/ger': Gerente = Att.replace('_', ' ')
                    case '/germ': Gerente = Att.replace('_', ' ')
                    case '/regional': Gerente = Att.replace('_', ' ')
                    case '/regionalm': Gerente = Att.replace('_', ' ')
                    case '/reg': Gerente = Att.replace('_', ' ')
                    case '/regm': Gerente = Att.replace('_', ' ')
                    
                CR = valor[1]

                match tipo:
                    case 1: consCr = f"""SELECT 
                T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN Recurso R
                    on R.CodigoHash = T.ModificadoPorHash
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                    on ES.Id_Estrutura = T.EstruturaId
                WHERE Es.CRNo = {CR}
                AND T.Expirada = 0
                AND T.Nome LIKE '%{Att}%'
                AND T.Status = 85
                AND DAY(TerminoReal) = {day}
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.Nome, R.Nome
                ORDER BY [Total] DESC"""
                    case 2: consCr = f"""SELECT 
                T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN Recurso R
                    on R.CodigoHash = T.ModificadoPorHash
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                    on ES.Id_Estrutura = T.EstruturaId
                WHERE Es.CRNo = {CR}
                AND T.Expirada = 0
                AND T.Nome LIKE '%{Att}%'
                AND T.Status = 85
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.Nome, R.Nome
                ORDER BY [Total] DESC"""
                    case 3: consCr = f"""SELECT
                    T.EstruturaNivel2 as 'CR',
                    COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA as Es
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr
                    on cr.ID_CR = Es.Id_CR
                WHERE cr.Gerente = '{Gerente}'
                AND T.Expirada = 0
                AND T.Status = 85
                AND DAY(TerminoReal) = {day}
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.EstruturaNivel2
                ORDER BY [Total] DESC
                """
                    case 4: consCr = f"""SELECT
                    T.EstruturaNivel2 as 'CR',
                    COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA as Es
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr
                    on cr.ID_CR = Es.Id_CR
                WHERE cr.Gerente = '{Gerente}'
                AND T.Expirada = 0
                AND T.Status = 85
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.EstruturaNivel2
                ORDER BY [Total] DESC
                """
                    case 5: consCr = f"""SELECT
                    T.EstruturaNivel2 as 'CR',
                    COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA as Es
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr
                    on cr.ID_CR = Es.Id_CR
                WHERE cr.GerenteRegional = '{Gerente}'
                AND T.Expirada = 0
                AND T.Status = 85
                AND DAY(TerminoReal) = {day}
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.EstruturaNivel2
                ORDER BY [Total] DESC
                """
                    case 6: consCr = f"""SELECT
                    T.EstruturaNivel2 as 'CR',
                    COUNT(T.Nome) as 'Total'
                FROM Tarefa T
                INNER JOIN DW_Vista.dbo.DM_ESTRUTURA as Es
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr
                    on cr.ID_CR = Es.Id_CR
                WHERE cr.GerenteRegional = '{Gerente}'
                AND T.Expirada = 0
                AND T.Status = 85
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.EstruturaNivel2
                ORDER BY [Total] DESC
                """
                        
                df = read_sql_query(consCr, self.conn)
                export(df, 'temp.png', max_rows=90, max_cols=10)
                
                img = bot.send_photo(chat_id=msg.chat.id, photo=open('temp.png', 'rb'))
                if tipo < 3: bot.reply_to(img, f'Segue consulta referente ao contrato {CR} no periodo {now}')
                if tipo >= 3: bot.reply_to(img, f'Segue consulta referente a Gerencia {Gerente} no periodo {now}')

            except Exception as error: bot.reply_to(msg, f'Erro com a consulta ❌: \n {error}')

cns = CNS()

# Inicio
@bot.message_handler(commands=['start','começar','init'])             
def CNS_boasvindas(msg):
    bot.reply_to(msg, msgP.boas_vindas.replace('$$USER', msg.from_user.first_name))

# Consultar Total de Tarefas Dia
@bot.message_handler(commands=['total','const'])
def CNS_consultar(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=1)

# Consultar Total de Tarefas Mês
@bot.message_handler(commands=['totalm', 'constm'])
def CNS_consultar(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=2)

# Gerencia DIA
@bot.message_handler(commands=['gerente','ger'])
def CNS_gerencia(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=3)

# Gerencia MES
@bot.message_handler(commands=['gerentem','germ'])
def help_us(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=4)

# GerenciaRegional DIA
@bot.message_handler(commands=['regional','reg'])
def help_us(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=5)

# GerenciaRegional MES
@bot.message_handler(commands=['regionalm','regm'])
def help_us(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg, tipo=6)

# HELP US
@bot.message_handler(commands=['help','ajuda'])
def help_us(msg):
    bot.reply_to(msg, msgP.help)

# Qualquer outra mensagem
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, msgP.diversos)

try: system('cls')
except: system('clear')

print('CNS-Bot em execução!...')
bot.infinity_polling()

