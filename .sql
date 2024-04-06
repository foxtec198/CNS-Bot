SELECT R.Nome, COUNT(R.Nome) as 'Total'
FROM Tarefa T with(nolock)
INNER JOIN Recurso R with(nolock)
    on R.CodigoHash = T.FinalizadoPorHash
INNER JOIN dw_vista.dbo.DM_ESTRUTURA Es with(nolock)
    on Es.Id_Estrutura = T.EstruturaId
INNER JOIN DW_Vista.dbo.DM_CR cr with(nolock)
    on cr.Id_CR = Es.Id_CR
WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
AND T.Nome LIKE '%Visita%'
AND R.Nome <> 'Sistema'
AND MONTH(T.TerminoReal) = 03
AND YEAR(T.TerminoReal) = 2024
GROUP BY R.Nome
ORDER BY COUNT(R.Nome) DESC