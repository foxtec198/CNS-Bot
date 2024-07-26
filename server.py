import telebot
import msgP
from pandas import read_sql_query
from dataframe_image import export
from time import strftime as st
from os import system
from qrcode import QRCode
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from PIL import Image
import yaml

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

    def data(self):
        self.now = st('%x - %X')
        self.day = st('%d')
        self.month =st('%m')
        self.year = st('%Y')

    def gerarPng(self, conn, consulta, arquivo='temp.png'):
        df = read_sql_query(consulta, conn)
        export(df, filename=arquivo, max_cols=-1, max_rows=-1)
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

    def consultar(self, msg, tipo=None):
        now = st('%d-%m-%Y %H:%M')
        self.data()
        valor = msg.text.split()
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
            AND DAY(TerminoReal) = {self.day}
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
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
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
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
            AND DAY(TerminoReal) = {self.day}
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
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
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
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
            AND DAY(TerminoReal) = {self.day}
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
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
            AND MONTH(TerminoReal) = {self.month}
            AND YEAR(TerminoReal) = {self.year}
            GROUP BY T.EstruturaNivel2
            ORDER BY [Total] DESC
            """
            
            engine = cns.connect(uid, pw, server)
            conn = engine.connect()

            
            img = bot.send_photo(
                chat_id = msg.chat.id, 
                photo = open(
                    self.gerarPng(conn, consCr), 'rb'
                    )
                )

            if tipo < 3: bot.reply_to(img, f'Segue consulta referente ao contrato {CR} no periodo {now}')
            elif tipo >= 3: bot.reply_to(img, f'Segue consulta referente a Gerencia {Gerente} no periodo {now}')
        except Exception as error: bot.reply_to(msg, f'Erro encontrado ❌: \n {error}')

    def cns_qrcode(self, msg):
        msg2 = msg.text.split()
        param = msg2[1].split(':')
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
        try:
            engine = cns.connect(uid, pw, server)
            conn = engine.connect()
            qr.gerar(cr, 'LIKE','>=', Nivel, Empresa, 'Locais', conn)
            nomeArquivo = f'QRCodes/{self.qr.nomeCR}.pdf'
            arquivo = open(nomeArquivo, 'rb')
            arq = bot.send_document(chat_id=msg.chat.id, document=arquivo)
            bot.reply_to(arq, f'Segue QRCodes - {self.qr.nomeCR}')
        except Exception as e: bot.reply_to(msg, str(e))

    def cons_visita(self, msg): 
        self.data() # Atualiza as datas 
        param = msg.text.split()
        match len(param):
            case 1: 
                bot.reply_to(msg, 'Consultando visitas referente ao mes atual!')
                cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {self.month}
                AND YEAR(T.TerminoReal) = {self.year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""
            case 2: 
                month = param[1]
                bot.reply_to(msg, f'Consultando visitas referente a data {month}!')
                cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                FROM Tarefa T with(nolock)
                INNER JOIN Recurso R with(nolock)
                    on R.CodigoHash = T.FinalizadoPorHash
                INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                    on Es.Id_Estrutura = T.EstruturaId
                INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                    on cr.Id_CR = Es.Id_CR
                WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
                AND T.ChecklistId in (
                    '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
                    '21368b38-a8f5-4793-8317-aca40a9489a5',
                    '71bb4fa9-6f30-45df-9461-4b01534fbc12',
                    'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
                    '460e6d74-a6fe-4128-bc84-3d0455d30f45'
                )
                AND R.Nome <> 'Sistema'
                AND MONTH(T.TerminoReal) = {month}
                AND YEAR(T.TerminoReal) = {self.year}
                GROUP BY R.Nome
                ORDER BY COUNT(R.Nome) DESC"""
        
        engine = cns.connect(uid, pw, server)
        conn = engine.connect()

        img = bot.send_photo(
            chat_id=msg.chat.id, 
            photo=open(
                self.gerarPng(conn, cons),'rb'
                )
            )
        bot.reply_to(img, 'Segue visitas realizadas! 🥈✅')

with open('utils/cred.yaml', 'r') as f: cred = yaml.load(f, yaml.FullLoader)
creds = []
for i in cred:
    creds.append(cred[i])
uid, pw, server, API = creds

cns = CNS()
bot = telebot.TeleBot(API)
qr = QRCode()

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

@bot.message_handler(commands=['qrcode', 'qr'])
def qrcode(msg):
    cns.cns_qrcode(msg)

@bot.message_handler(commands=['visita'])
def cons_visita(msg):
    cns.cons_visita(msg)

# Qualquer outra mensagem
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, msgP.diversos)

try: system('cls')
except: system('clear')

print('CNS-Bot em execução!...')
bot.infinity_polling()

