help = """
/total CR(SOMENTE NUMEROS) TAREFA(OPCIONAL) -- Total do dia atual 
/totalm CR(SOMENTE NUMEROS) TAREFA(OPCIONAL)-- Total do mês atual
/gerente NOME_DO_GERENTE -- Total por CR e Gerência do dia atual
/gerentem NOME_DO_GERENTE -- Total por CR e Gerência do mês atual
/regional NOME_DO_GERENTE -- Total por CR e Gerência do dia atual
/regionalm NOME_DO_GERENTE -- Total por CR e Gerência do mês atual
/qrcode CR(SOMENTE NUMEROS):NIVEL:LOGO(Poliservice, Grupo GPS, In Haus, Topservice)
OBS: O nivel 1 é considerado como PEC, o 2 Grupo de Cliente e o 3 como CR, o que vier após é considerado como uma nova contagem, Ex: 4 = 1, 5 = 2 e assim por diante! 
"""

boas_vindas = f'''
Olá $$USER seja bem-vindo ao CNS.
Para realizar uma consulta basta usar os comandos abaixo!
{help}
'''

diversos = f'''
Comando não encontrado.. 😢
Por favor use uma das consultas abaixo:
{help}
'''
