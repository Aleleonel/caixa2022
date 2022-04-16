select 
	entrada, saida, 
    (entrada -saida) estoque
from     
(
	(SELECT 
		sum(e.estoque) entrada
	FROM estoque e 
	where e.idproduto = 1 
	and e.status = 'E') entrada,  
	(SELECT 
		sum(e.estoque) saida
	FROM estoque e 
	where e.idproduto = 1 
	and e.status = 'S') saida 
)