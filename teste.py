def cns_qrcode(msg):
    msg2 = msg.split(' ')
    param = msg2[1].split(':')
    CR = param[0]
    if len(param) == 2: Nivel = param[1]
    else: Nivel = 3

cns_qrcode('/qrcode 42636:5')