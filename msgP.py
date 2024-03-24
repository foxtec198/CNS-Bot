help = """
/total CR(SOMENTE NUMEROS) TAREFA(OPCIONAL) -- Retorna o total do dia atual 
/totalm CR(SOMENTE NUMEROS) TAREFA(OPCIONAL)-- Retorna o total do mês atual

Caso queira pra usar a data personalizada, coloque dia mes ou ano separado como no exemplo abaixo:
/total 12345 NomeTarefa 20 03 2024 -- Neste exemplo ele ira retornar o que foi realizado dia 20/03/2024 da Tarefa "NomeTarefa" do CR "12345"  
/totalm 12345 NomeTarefa 03 2024 -- Neste exemplo ele ira retornar o que foi realizado mês 03/2024 da Tarefa "NomeTarefa" do CR "12345"  
"""

boas_vindas = f'''
Olá $$USER seja bem-vindo ao CNS.
Para realizar uma consulta basta as consultas abaixo!
{help}
'''

diversos = f'''
Comando não encontrado.. 😢
Por favor use uma das consultas abaixo:
{help}
'''
