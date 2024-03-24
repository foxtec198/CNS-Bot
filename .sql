select T.Nome, COUNT(T.Nome) as 'Total'
from Tarefa T
inner join DW_Vista.dbo.DM_ESTRUTURA ES
    on ES.Id_Estrutura = T.EstruturaId
WHERE Es.CRNo = 42636
AND DAY(TerminoReal) = 23
AND MONTH(TerminoReal) = 03
AND YEAR(TerminoReal) = 2024
GROUP BY T.Nome