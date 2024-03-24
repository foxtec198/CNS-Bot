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

    def consultar(self, msg, day=None, month=None, year=None):
        now = st('%X - %x')
        if not day: day = st('%d')
        if not month: month =st('%m')
        if not year: year = st('%Y')

        c = self.Conn(msg, 'guilherme.breve','84584608@Gui')
        if c:
            valor = msg.text.split()
            try:
                CR = valor[1]
                bot.reply_to(msg, f'Consultando {CR}...')

                consCr = f"""select T.Nome, COUNT(T.Nome) as 'Total'
                from Tarefa T
                inner join DW_Vista.dbo.DM_ESTRUTURA ES
                    on ES.Id_Estrutura = T.EstruturaId
                WHERE Es.CRNo = {CR}
                AND DAY(TerminoReal) = {day}
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
@bot.message_handler(commands=['start'])             
def CNS_boasvindas(msg):
    bot.reply_to(msg, msgP.boas_vindas.replace('$$USER', msg.from_user.first_name))

# Consultar
@bot.message_handler(commands=['consultar'])
def CNS_consultar(msg):
    bot.reply_to(msg, 'Só um instante')
    cns.consultar(msg)

# Qualquer outra mensagem
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, msgP.diversos)

bot.infinity_polling()  
