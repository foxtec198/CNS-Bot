import telebot
import msgP
from pandas import read_sql_query
from dataframe_image import export
from time import strftime as st
from os import system
from qrcode import QRCode

API  = '7134052176:AAHfgBxarhx3wj5N8sTtFNRawuWt3PaXv0k'
bot = telebot.TeleBot(API)

# Conectar
class CNS:
    def connect(self, user = 'guilherme.breve', pwd='84584608@Gui', server='10.56.6.56'):
        try:
            self.qr = QRCode(user, pwd, server)
            self.conn = self.qr.conn
            return True
        except: return False

    def data(self):
        self.now = st('%x - %X')
        self.day = st('%d')
        self.month =st('%m')
        self.year = st('%Y')

    def consultar(self, msg, tipo=None):
        self.data()

        if self.connect():
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
                        
                df = read_sql_query(consCr, self.conn)
                export(df, 'temp.png', max_rows=90, max_cols=10)
                
                img = bot.send_photo(chat_id=msg.chat.id, photo=open('temp.png', 'rb'))
                if tipo < 3: bot.reply_to(img, f'Segue consulta referente ao contrato {CR} no periodo {now}')
                elif tipo >= 3: bot.reply_to(img, f'Segue consulta referente a Gerencia {Gerente} no periodo {now}')

            except Exception as error: 
                bot.reply_to(msg, f'Erro com a consulta ❌: \n {error}')

    def cns_qrcode(self, msg):
        self.connect()
        msg2 = msg.text.split()
        param = msg2[1].split(':')
        cr = param[0]
        if len(param) >= 2: Nivel = param[1]
        else: Nivel = 3
        if len(param) == 3: Empresa = param[2]
        else: Empresa = 'Grupo GPS'
        bot.reply_to(msg, f'Criando QRCode do contrato {cr}, no Nivel {Nivel}, com a logo da empresa {Empresa}, Um instante. ✅')
        try:
            self.qr.gerar(cr, 'LIKE','>=', Nivel, Empresa, 'Locais')
            nomeArquivo = f'QRCodes/{self.qr.nomeCR}.pdf'
            arquivo = open(nomeArquivo, 'rb')
            arq = bot.send_document(chat_id=msg.chat.id, document=arquivo)
            bot.reply_to(arq, f'Segue QRCodes - {self.qr.nomeCR}')
        except Exception as e: bot.reply_to(msg, str(e))

    def cons_visita(self, msg):
        self.data() # Atualiza as datas 
        param = msg.split()
        if self.connect():
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
                    AND T.Nome LIKE '%Visita%'
                    AND R.Nome <> 'Sistema'
                    AND MONTH(T.TerminoReal) = {self.month}
                    AND YEAR(T.TerminoReal) = {self.year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC"""
                case 2: 
                    data = param.split('_')
                    day = data[0]
                    month = data[1]
                    bot.reply_to(msg, f'Consultando visitas referente a data {data}!')
                    cons = f"""SELECT R.Nome, COUNT(R.Nome) as 'Total'
                    FROM Tarefa T with(nolock)
                    INNER JOIN Recurso R with(nolock)
                        on R.CodigoHash = T.FinalizadoPorHash
                    INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
                        on Es.Id_Estrutura = T.EstruturaId
                    INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
                        on cr.Id_CR = Es.Id_CR
                    WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
                    AND T.Nome LIKE '%Visita%'
                    AND R.Nome <> 'Sistema'
                    AND DAY(T.TerminoReal) = {day}
                    AND MONTH(T.TerminoReal) = {month}
                    AND YEAR(T.TerminoReal) = {self.year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC"""

            dados = read_sql_query(cons, self.conn)
            export(dados, 'temp.png', max_cols=5, max_rows=99)
            img = bot.send_photo(chat_id=msg.chat.id, photo=open('temp.png','rb'))
            bot.reply_to(img, 'Segue visitas realizadas! 🥈✅')

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

