import telebot
import msgP
from pyodbc import connect
from pandas import read_sql
from dataframe_image import export
from time import strftime as st

API  = '7134052176:AAHfgBxarhx3wj5N8sTtFNRawuWt3PaXv0k'
bot = telebot.TeleBot(API)

# Conectar
class CNS:
    def Conn(self, msg, user, pwd, server='10.56.6.56',db='Vista_Replication_PRD'):
        try:
            self.conn = connect(f'DRIVER=SQL Server;SERVER={server};UID={user};PWD={pwd};DATABASE={db}')
            bot.reply_to(msg, f'{msg.from_user.first_name} - Conexão Ativa')
            return True
        except Exception as error:
            bot.reply_to(msg, f"""Conexão Invalida: {error}""")
            return False

    def consultar(self, msg, tipo=None):
        now = st('%X - %x')
        day = st('%d')
        month =st('%m')
        year = st('%Y')

        c = self.Conn(msg, 'guilherme.breve','84584608@Gui')
        if c:
            valor = msg.text.split()
            try:
                CR = valor[1]
                if valor[2]: 
                    Tarefa = valor[2]
                    if valor[3]: day = valor[3]
                    if valor[4]: month = valor[4]
                    if valor[5]: day = valor[5]
                else: 
                    Tarefa = ''
                    if valor[2]: day = valor[2]
                    if valor[3]: month = valor[3]
                    if valor[4]: day = valor[4]

                match tipo:
                    case 1: consCr = f"""select T.Nome, COUNT(T.Nome) as 'Total'
                from Tarefa T
                inner join DW_Vista.dbo.DM_ESTRUTURA ES
                    on ES.Id_Estrutura = T.EstruturaId
                WHERE Es.CRNo = {CR}
                AND T.Nome LIKE '%{Tarefa}%'
                AND DAY(TerminoReal) = {day}
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.Nome"""
                    case 2: consCr = f"""select T.Nome, COUNT(T.Nome) as 'Total'
                from Tarefa T
                inner join DW_Vista.dbo.DM_ESTRUTURA ES
                    on ES.Id_Estrutura = T.EstruturaId
                WHERE Es.CRNo = {CR}
                AND T.Nome LIKE '%{Tarefa}%'
                AND MONTH(TerminoReal) = {month}
                AND YEAR(TerminoReal) = {year}
                GROUP BY T.Nome"""
                        
                df = read_sql(consCr, self.conn)
                export(df, 'temp.png')
                
                img = bot.send_photo(chat_id=msg.chat.id, photo=open('temp.png', 'rb'))
                bot.reply_to(img, f'Segue consulta referente ao contrato {CR} na data {now}')

            except Exception as error: bot.reply_to(msg, f'Erro com a consulta \n {error}')

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

# Qualquer outra mensagem
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, msgP.diversos)

print('CNS-Bot em execução!')
bot.infinity_polling()  
