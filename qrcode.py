from pandas import read_sql_query
from functools import cache
from PIL import Image, ImageDraw, ImageFont
from shutil import rmtree
from segno import make
from reportlab.pdfgen import canvas
from os import listdir
from PyPDF2 import PdfMerger, PdfReader
from backEnd import BackEnd
from os import mkdir

class QRCode:
    def __init__(self, user, pwd, server):
        b = BackEnd()
        c = b.connect_db(user, pwd, server)
        if c == 'Conectado': 
            self.conn = b.conn
    @cache
    def get_empresas(self, empresas):
        match empresas:
            case 'Poliservice': return 'src/logos/poliservice.png'
            case 'Top Service': return 'src/logos/topservice.png'
            case 'Grupo GPS': return 'src/logos/ggps.png'
            case 'In Haus': return 'src/logos/inhaus.png'
    @cache
    def get_cr(self, numCR):
        try:
            cr = read_sql_query(f"SELECT TOP 1 Descricao FROM ESTRUTURA WHERE HierarquiaDescricao LIKE '%{numCR}%'", self.conn)
            for i in cr['Descricao']:
                return i
        except: return 'CR não corresponde'
    @cache
    def definir_cor(self, cr):
        # Azul claro limpeza, laranja logistica, vermelho manutenção, azul escuro segurança e verde jardinagem
        if 'POR -' in cr: return 'src/cores/modeloCinza.png'
        elif 'MAV -' in cr: return 'src/cores/modeloVerde.png'
        elif 'MAP -' in cr: return 'src/cores/modeloVermelho.png'
        elif 'LPG -' in cr: return 'src/cores/modeloAzul.png'
        elif 'SEG -' in cr: return 'src/cores/modeloAzulEscuro.png'
        else: return 'src/cores/modeloAzulEscuro.png'
    @cache
    def  cons(self, cr, op_cr, nivel, op_nivel, tipos):
        match tipos:
            case 'Ativos': tipo = 'A'
            case 'Locais': tipo = 'L'
            case 'Ambos': tipo = ''

        match op_cr:
            case 'LIKE': return read_sql_query(f"""
            SELECT 
            Es.QRCode,
            Es.Descricao,
            Es.Id,
            (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior' 
            FROM Estrutura ES
            WHERE HierarquiaDescricao LIKE '%{cr}%'
            AND Es.Tipo LIKE '%{tipo}%'
            AND Nivel {nivel} {op_nivel}""", self.conn)
            
            case '=': return read_sql_query(f"""SELECT
            Es.QRCode,
            Es.Descricao,
            Es.Id,
            (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
            FROM Estrutura ES
            INNER JOIN dw_vista.dbo.DM_ESTRUTURA E
            ON E.ID_Estrutura = Es.Id
            WHERE E.CRno = {cr}
            AND Es.Tipo = '%{tipo}%'
            AND Es.Nivel {nivel} {op_nivel}""", self.conn)

    def get_link_estrutura(self, id):
        return f'https://inteligenciaoperacional.app.br/report/gpsvista.php?qrcode={id}'
          
    def resizeImg(self, img, valor: tuple):
        imgR = Image.open(img)
        imgR.thumbnail(valor)
        imgR.save(img)

    def gerar(self, cr, op_cr, nivel, op_nivel, empresa, tipos):
        if cr != '':
            try:
                mkdir('src/temp')
                mkdir('./QRCodes')
            except: ...
            nomeCR = self.get_cr(cr)
            self.nomeCR = nomeCR
            estrutura = self.cons(cr, op_cr, nivel, op_nivel, tipos)
            es = estrutura.to_dict()
            for i in es['Descricao']:
                local = es['Descricao'][i]
                superior = es['Superior'][i]
                link = self.get_link_estrutura(es['Id'][i])
                qr = es['QRCode'][i]
                self.makePng(nomeCR, local, qr, link, i, empresa, superior)
                self.merge(nomeCR)
            rmtree('src/temp')
    
    def makePng(self, crNome, local, qr, link, cont, empresas, superior):
            # Gera os QR Codes
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
            txt = f'{crNome[:40]}\n{crNome[40:]}'
            textImg.text((450, 150), txt, font=fnt, fill='black', align='center')

            # TEXTO - Nome Local
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('arial', 20)
            txt = f'{superior} > {local[:20]}\n{local[20:]}'
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

if __name__ == '__main__':
    qr = QRCode('guilherme.breve','84584608@Gui','10.56.6.56')
    qr.gerar(cr=42636, op_cr='=', op_nivel=3, nivel='>=', empresa='Grupo GPS')
