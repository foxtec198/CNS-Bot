-- select T.Nome, COUNT(T.Nome) as 'Total'
-- from Tarefa T
-- inner join DW_Vista.dbo.DM_ESTRUTURA ES
--     on ES.Id_Estrutura = T.EstruturaId
-- WHERE Es.CRNo = 11930
-- AND T.Nome LIKE '%%'
-- AND T.Status = 85
-- AND T.Expirada = 0
-- AND DAY(TerminoReal) = 25
-- AND MONTH(TerminoReal) = 03
-- AND YEAR(TerminoReal) = 2024
-- GROUP BY T.Nome
-- ORDER BY [Total] DESC

SELECT
    T.EstruturaNivel2 as 'CR',
    COUNT(T.Nome) as 'Total'
FROM Tarefa T
INNER JOIN DW_Vista.dbo.DM_ESTRUTURA as Es
    on Es.Id_Estrutura = T.EstruturaId
INNER JOIN DW_Vista.dbo.DM_CR cr
    on cr.ID_CR = Es.Id_CR
WHERE cr.Gerente LIKE '%DENISE DOS%'
AND DAY(TerminoReal) = 25
AND MONTH(TerminoReal) = 03
AND YEAR(TerminoReal) = 2024
GROUP BY T.EstruturaNivel2
ORDER BY [Total] DESC

