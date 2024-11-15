import telebot
import models.msgP as msgP
from pandas import read_sql_query
from dataframe_image import export
from os import system
from utils.qrcode import QRCode
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from PIL import Image
from datetime import datetime as dt
from utils.get_fb import req

# Conectar
class CNS:
    def connect(self, uid, pwd, server, database='Vista_Replication_PRD', driver='ODBC Driver 18 for SQL Server'):
        self.uid = quote_plus(uid)
        self.pwd = quote_plus(pwd)
        self.server = quote_plus(server)
        self.database = quote_plus(database)
        driver = quote_plus(driver)
        url = f'mssql://{self.uid}:{self.pwd}@{self.server}/{self.database}?driver={driver}&&TrustServerCertificate=yes'
        try:
            engine = create_engine(url)
            return engine
        except Exception as error: return error

    def gerarPng(self, conn, consulta, arquivo='temp.png'):
        df = read_sql_query(consulta, conn)
        export(df, filename=arquivo, max_cols=-1, max_rows=-1, table_conversion='selenium')
        dt = Image.open(arquivo)
        logo = Image.open('GPS.png')
        hm = dt.size[1] + logo.size[1] 
        wm = dt.size[0]
        modelo = Image.new('RGBA', (wm, hm), color='#DFDFDF')
        mid = int(modelo.width/2) - int(logo.width/2)
        modelo.paste(logo, (mid, 0), logo)
        modelo.paste(dt, (0, logo.height + 1))
        modelo.save(arquivo)
        return arquivo

    def cns_qrcode(self, msg):
        try:
            param = msg.text
            param =  param.replace('/qr ','')
            param =  param.replace('/qrcode ','')
            param = param.split(':')
            cr = param[0]
            if len(param) >= 2:
                Nivel = param[1]
                match Nivel:
                    case '': Nivel = 3
                    case ' ': Nivel = 3
            else: Nivel = 3
            if len(param) == 3: Empresa = param[2]
            else: Empresa = 'Grupo GPS'
            bot.reply_to(msg, f'Criando QRCode do contrato {cr}, no Nivel {Nivel}, com a logo da empresa {Empresa}, Um instante. ✅')
            engine = cns.connect(uid, pw, server)
            with engine.connect() as conn:
                nomeArquivo = qr.gerar(cr, '>=', Nivel, Empresa, 'Locais', conn)
                if 'QRCodes/' in nomeArquivo:
                    arquivo = open(nomeArquivo, 'rb')
                    arq = bot.send_document(chat_id=msg.chat.id, document=arquivo)
                    bot.reply_to(arq, f'Segue QRCodes - {qr.nomeCR}')
                else: bot.reply_to(msg, f'Erro encontrado: {nomeArquivo}')
        except Exception as e: bot.reply_to(msg, f'Erro ao Gerar QR: {e}')

uid = req['uid'].strip()
server = req['server'].strip()
API = req['API'].strip()
pw = req['pw'].strip()

cns = CNS()
bot = telebot.TeleBot(API)
qr = QRCode()
eg = cns.connect(uid, pw, server) # Cria a engine de conexão

# Inicio
@bot.message_handler(commands=['start','init'])             
def CNS_boasvindas(msg):
    bot.reply_to(msg, msgP.boas_vindas.replace('$$USER', msg.from_user.first_name))

# Consultar Total de Tarefas Dia
@bot.message_handler(commands=['total','tt'])
def CNS_consultar(msg):
    bot.reply_to(msg, 'Só um instante')
    try:
        data = dt.now() # Data atual
        # Separa por categorias
        day = data.strftime('%d')
        month = data.strftime('%m')
        year = data.strftime('%Y')

        # Separa CR de Tarefa(Caso haja)
        valor = msg.text
        valor = valor.replace('/total ','')
        valor = valor.replace('/tt ','')
        valor = valor.split(':')
        
        match len(valor):
            case 1:
                cons = F'''SELECT T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                        FROM Tarefa T
                        INNER JOIN Recurso R
                            on R.CodigoHash = T.ModificadoPorHash
                        INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                            on ES.Id_Estrutura = T.EstruturaId
                        WHERE Es.CRNo = '{valor[0]}'
                        AND T.Expirada = 0
                        AND T.Status = 85
                        AND DAY(TerminoReal) = {day}
                        AND MONTH(TerminoReal) = {month}
                        AND YEAR(TerminoReal) = {year}
                        GROUP BY T.Nome, R.Nome
                        ORDER BY [Total] DESC'''
            case 2:
                cons = F'''SELECT T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                        FROM Tarefa T
                        INNER JOIN Recurso R
                            on R.CodigoHash = T.ModificadoPorHash
                        INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                            on ES.Id_Estrutura = T.EstruturaId
                        WHERE Es.CRNo = '{valor[0]}'
                        AND T.Expirada = 0
                        AND T.Status = 85
                        AND DAY(TerminoReal) = {day}
                        AND MONTH(TerminoReal) = {month}
                        AND YEAR(TerminoReal) = {year}
                        AND T.Nome LIKE '%{valor[1]}%'
                        GROUP BY T.Nome, R.Nome
                        ORDER BY [Total] DESC'''
        
        with eg.connect() as conn: # Conecta ao DB
            cns.gerarPng(conn, cons) # Gera o PNG com as Logos

        # Envia a imagem
        ph = bot.send_photo(msg.chat.id, open('temp.png', 'rb'))
        bot.reply_to(ph, f"""Segue consulta do contrato {valor[0]} \n\n Data: {data.strftime('%d/%m/%Y - %H:%M')}""")

    except Exception as e: bot.send_message(chat_id=msg.chat.id, text=f'Erro: {e}')

# Consultar Total de Tarefas Mês
@bot.message_handler(commands=['totalm', 'tm'])
def CNS_consultar(msg):
    bot.reply_to(msg, 'Só um instante')
    try:
        data = dt.now() # Data atual
        # Separa por categorias
        month = data.strftime('%m')
        year = data.strftime('%Y')

        # Separa CR de Tarefa(Caso haja)
        valor = msg.text
        valor = valor.replace('/totalm ','')
        valor = valor.replace('/tm ','')
        valor = valor.split(':')
        
        match len(valor):
            case 1:
                cons = F'''SELECT T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                        FROM Tarefa T
                        INNER JOIN Recurso R
                            on R.CodigoHash = T.ModificadoPorHash
                        INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                            on ES.Id_Estrutura = T.EstruturaId
                        WHERE Es.CRNo = '{valor[0]}'
                        AND T.Expirada = 0
                        AND T.Status = 85
                        AND MONTH(TerminoReal) = {month}
                        AND YEAR(TerminoReal) = {year}
                        GROUP BY T.Nome, R.Nome
                        ORDER BY [Total] DESC'''
            case 2:
                cons = F'''SELECT T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
                        FROM Tarefa T
                        INNER JOIN Recurso R
                            on R.CodigoHash = T.ModificadoPorHash
                        INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
                            on ES.Id_Estrutura = T.EstruturaId
                        WHERE Es.CRNo = '{valor[0]}'
                        AND T.Expirada = 0
                        AND T.Status = 85
                        AND MONTH(TerminoReal) = {month}
                        AND YEAR(TerminoReal) = {year}
                        AND T.Nome LIKE '%{valor[1]}%'
                        GROUP BY T.Nome, R.Nome
                        ORDER BY [Total] DESC'''
        
        with eg.connect() as conn: # Conecta ao DB
            cns.gerarPng(conn, cons) # Gera o PNG com as Logos

        # Envia a imagem
        ph = bot.send_photo(msg.chat.id, open('temp.png', 'rb'))
        bot.reply_to(ph, f"""Segue consulta do contrato {valor[0]} \n\n Data: {data.strftime('%d/%m/%Y - %H:%M')}""")

    except Exception as e: bot.send_message(chat_id=msg.chat.id, text=f'Erro: {e}')

# HELP US
@bot.message_handler(commands=['help','ajuda'])
def help_us(msg):
    bot.reply_to(msg, msgP.help)

# Gerar QR Codes
@bot.message_handler(commands=['qrcode', 'qr'])
def qrcode(msg):
    cns.cns_qrcode(msg)

# Consultar Visitas (Mes Atual ou Desejado)
@bot.message_handler(commands=['visita'])
def cons_visita(msg):
    try:
        data = dt.now() # Data atual
        # Separa por categorias
        month = data.strftime('%m')
        year = data.strftime('%Y')

        valor = msg.text
        valor = valor.replace('/visita','')
        params = valor.split(':')
        gerente = params[0].strip().upper()

        if len(params) == 1:
            bot.reply_to(msg, f'Consultando visitas referente ao mes atual, do(a) gerente {gerente}, Aguarde!')
            cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.Gerente like '%{gerente}'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {month}
                AND YEAR(T.TerminoReal) = {year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""
        elif len(params) == 2:
            monthP = int(params[1])
            bot.reply_to(msg, f'Consultando visitas referente ao mês {monthP}, do(a) gerente {gerente}, Aguarde!')
            cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.Gerente like '%{gerente}'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {monthP}
                AND YEAR(T.TerminoReal) = {year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""

        with eg.connect() as conn:
            cns.gerarPng(conn, cons)

        ph = bot.send_photo(msg.chat.id, open('temp.png', 'rb'))
        bot.reply_to(ph, 'Segue visitas realizadas! 🥈✅')
    except Exception as err: bot.reply_to(msg, f'Erro encontrado: {err}')
    
# Consultar Visitas (Mes Atual ou Desejado)
@bot.message_handler(commands=['visitaR'])
def cons_visitaR(msg):
    try:
        data = dt.now() # Data atual
        # Separa por categorias
        month = data.strftime('%m')
        year = data.strftime('%Y')

        valor = msg.text
        valor = valor.replace('/visitaR','')
        params = valor.split(':')
        gerente = params[0].strip().upper()

        if len(params) == 1:
            bot.reply_to(msg, f'Consultando visitas referente ao mes atual, do(a) Regional {gerente}, Aguarde!')
            cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.GerenteRegional like '%{gerente}'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {month}
                AND YEAR(T.TerminoReal) = {year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""
        elif len(params) == 2:
            monthP = int(params[1])
            bot.reply_to(msg, f'Consultando visitas referente ao mês {monthP}, do(a) Regional {gerente}, Aguarde!')
            cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.GerenteRegional like '%{gerente}'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {monthP}
                AND YEAR(T.TerminoReal) = {year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""

        with eg.connect() as conn:
            cns.gerarPng(conn, cons)

        ph = bot.send_photo(msg.chat.id, open('temp.png', 'rb'))
        bot.reply_to(ph, 'Segue visitas realizadas! 🥈✅')
    except Exception as err: bot.reply_to(msg, f'Erro encontrado: {err}')
    
# Qualquer outra mensagem
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, msgP.diversos)

try: system('cls')
except: system('clear')
print('CNS-Bot em execução!...')
bot.infinity_polling()
