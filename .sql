SELECT 
T.Nome, R.Nome as 'Colaborador', COUNT(T.Nome) as 'Total'
FROM Tarefa T
INNER JOIN Recurso R
    on R.CodigoHash = T.ModificadoPorHash
INNER JOIN DW_Vista.dbo.DM_ESTRUTURA ES
    on ES.Id_Estrutura = T.EstruturaId
WHERE Es.CRNo = 11930
AND R.Nome NOT IN ('Sistema')
AND T.Nome LIKE '%%'
AND T.Status = 85
AND MONTH(TerminoReal) = 03
AND YEAR(TerminoReal) = 2024
GROUP BY T.Nome, R.Nome
ORDER BY [Total] DESC