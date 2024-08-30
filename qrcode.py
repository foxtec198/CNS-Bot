from pandas import read_sql
from functools import cache
from PIL import Image, ImageDraw, ImageFont
from shutil import rmtree
from segno import make
from reportlab.pdfgen import canvas
from os import listdir
from PyPDF2 import PdfMerger, PdfReader
from os import mkdir
from sqlalchemy import create_engine
from urllib.parse import quote_plus 
import pyodbc

class QRCode:
    def new_connect_db(self, uid, pwd, server, database='Vista_Replication_PRD', driver='ODBC Driver 18 for SQL Server'):
        self.uid = quote_plus(uid)
        self.pwd = quote_plus(pwd)
        self.server = quote_plus(server)
        self.database = quote_plus(database)
        driver = quote_plus(driver)
        url = f'mssql://{self.uid}:{self.pwd}@{self.server}/{self.database}?driver={driver}&&TrustServerCertificate=yes'
        engine = create_engine(url)
        try:
            self.conn = engine.connect()
            return 'Conectado'
        except Exception as e:
            return f'Confira os dados acima! - {e}'

    @cache
    def get_empresas(self, empresas):
        match empresas:
            case 'Poliservice': return 'src/logos/poliservice.png'
            case 'Topservice': return 'src/logos/topservice.png'
            case 'Grupo GPS': return 'src/logos/ggps.png'
            case 'In Haus': return 'src/logos/inhaus.png'
    @cache
    
    def get_cr(self, numCR):
        try:
            cr = read_sql(f"SELECT TOP 1 Descricao FROM ESTRUTURA WHERE HierarquiaDescricao LIKE '%{numCR} -%'", self.conn)
            for i in cr['Descricao']:
                return i
        except: return numCR
    
    @cache
    def definir_cor(self, cr):
        # Azul claro limpeza, laranja logistica, vermelho manutenção, azul escuro segurança e verde jardinagem
        if ' - POR - ' in cr: return 'src/cores/modeloAzulEscuro.png'
        elif ' - MAV - ' in cr: return 'src/cores/modeloVerde.png'
        elif ' - MAP -' in cr: return 'src/cores/modeloVermelho.png'
        elif ' - LPG -' in cr: return 'src/cores/modeloAzul.png'
        elif ' - SEG -' in cr: return 'src/cores/modeloAzulEscuro.png'
        else: return 'src/cores/modeloCinza.png'

    @cache
    def  cons(self, cr, nivel, op_nivel, tipos):
        match tipos:
            case 'Ativos': tipo = 'A'
            case 'Locais': tipo = 'L'
            case 'Ambos': tipo = ''

        match nivel:
            case '1 - PEC': nivel = 1
            case '2 - Grupo de Cliente': nivel = 2
            case '3 - CR': nivel = 3

        if tipos != 'Ambos': cs = f"""SELECT
            Es.QRCode,
            Es.Descricao,
            Es.Id,
            (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
            FROM Estrutura ES
            INNER JOIN DW_Vista.dbo.DM_ESTRUTURA DE 
                ON DE.ID_Estrutura = ES.Id
            WHERE DE.CRNO = {cr}
            AND Es.Tipo IN ('A','L')
            AND Es.Nivel {op_nivel} {nivel}"""
            
        else: cs = f"""SELECT
            Es.QRCode,
            Es.Descricao,
            Es.Id,
            (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
            FROM Estrutura ES
            INNER JOIN DW_Vista.dbo.DM_ESTRUTURA DE
                ON DE.ID_Estrutura = Es.Id
            WHERE DE.CRNO = {cr}
            AND Es.Tipo = '{tipo}' 
            AND Es.Nivel {op_nivel} {nivel}"""

        dddd = read_sql(cs, self.conn)
        return dddd

    def get_link_estrutura(self, id):
        return f'https://inteligenciaoperacional.app.br/report/gpsvista.php?qrcode={id}'
          
    def resizeImg(self, img, valor: tuple):
        imgR = Image.open(img)
        imgR.thumbnail(valor)
        imgR.save(img)

    def gerar(self, cr, op_nivel, nivel, empresa, tipos, conn):
        try:mkdir('src/temp')
        except: ...
        try:mkdir('./QRCodes')
        except: ...

        self.conn = conn
        nomeCR = self.get_cr(cr)
        self.nomeCR = nomeCR
        estrutura = self.cons(cr, nivel, op_nivel, tipos)
        es = estrutura.to_dict()
        for i in es['Descricao']:
            if es['Descricao']:
                local = es['Descricao'][i]
                superior = es['Superior'][i]
                link = self.get_link_estrutura(es['Id'][i])
                qr = es['QRCode'][i]
                self.makePng(nomeCR, local, qr, link, i, empresa, superior)
                self.merge(nomeCR)
        try: rmtree('src/temp')
        except Exception as e: return e
        return f'QRCodes/{nomeCR}.pdf'
    
    def all_crs(self, cr, op_cr, nivel, op_nivel, empresa, tipos):
        if cr == 0:
            print('Imprimindo CRs')
            estrutura = self.cons(cr, op_cr, nivel, op_nivel, tipos)
            es = estrutura.to_dict()
            for i in es['Descricao']:
                if es['Descricao']:
                    local = es['Descricao'][i]
                    print(f'Gerando {local}')
                    superior = es['Superior'][i]
                    link = self.get_link_estrutura(es['Id'][i])
                    qr = es['QRCode'][i]
                    nomeCR = local
                    self.makePng(nomeCR, local, qr, link, i, empresa, superior)
                    self.merge('All Crs')
            
    def makePng(self, crNome, local, qr, link, cont, empresas, superior):
            # Gera os QR Codes
            crNome = crNome.upper()
            superior = superior.upper()
            local = local.upper()

            qrlocal = make(qr)
            qrlast = make(link)

            qrlocal.save('src/temp/qrtemp.png', scale=10)
            qrlast.save('src/temp/qrtemp2.png', scale=10)

            self.resizeImg('src/temp/qrtemp.png', (260, 260))
            self.resizeImg('src/temp/qrtemp2.png', (150, 150))

            coresImg = Image.open(self.definir_cor(crNome))
            logoImg = Image.open(self.get_empresas(empresas))
            qrImg = Image.open('src/temp/qrtemp.png')
            qrImg2 = Image.open('src/temp/qrtemp2.png')

            # TEXTO - Nome CR
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('src/fonts/arial_narrow_7.ttf', 30)
            txt = f'{crNome[:40]}'
            textImg.text((450, 150), txt, font=fnt, fill='black', align='center')

            # TEXTO - Nome Local
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('arial', 20)
            if '- PR -' in superior: txt = f'{local}'
            else: txt = f'{superior} > {local[:40]}\n{local[40:]}'
            textImg.text((450, 210), txt, font=fnt, fill='black', align='center')

            # Cola as propriedas na imagem final
            newImage = Image.new('RGBA', coresImg.size)
            newImage.paste(coresImg)
            newImage.paste(logoImg, (420, 5))
            newImage.paste(qrImg, (75, 100))
            newImage.paste(qrImg2, (755, 410))
            newImage.save('src/temp/temp.png')

            imgQr = Image.open('src/temp/temp.png')
            nomePdf = f'src/temp/{cont}.pdf'
            arquivo = canvas.Canvas(nomePdf, pagesize=imgQr.size, )
            arquivo.drawImage('src/temp/temp.png', 0, 0)
            arquivo.save()

    def merge(self, cr):
        dir = listdir('src/temp/')
        PDF = PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'src/temp/{i}', 'rb') as pdf:
                    leitura = PdfReader(pdf)
                    PDF.append(leitura)
        PDF.write(f'QRCodes/{cr}.pdf')
        PDF.close()

    def cons_crs(self):
        df = read_sql('''SELECT DISTINCT Nivel_03 as cr
        FROM DW_Vista.dbo.DM_ESTRUTURA DE WITH(NOLOCK)
        INNER JOIN DW_Vista.dbo.DM_CR DC WITH(NOLOCK) ON DC.ID_CR = DE.ID_CR
        WHERE DC.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
        AND Nivel_03 <> 'Null' ''', self.conn)
        return df['cr']
        
if __name__ == '__main__':
    qr = QRCode()
    conn = qr.new_connect_db('guilherme.breve','84584608@Gui198','10.56.6.56')
    print(conn)
    print(qr.gerar('60434 - PR - LPG - COND SPAZIO LEOPOLDINA', 4, '>=', 'Grupo GPS', 'Locais'))