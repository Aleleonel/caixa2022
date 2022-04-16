select
	coalesce(entrada, 0), 
    coalesce(saida, 0), 
    coalesce((entrada -saida), 0) estoque
from   
(	
    (SELECT 
		sum(e.estoque) entrada, e.idproduto  
	FROM estoque e 		
	where status = 'E' 
    and idproduto = 1) entrada,  
	(SELECT 
		sum(e.estoque) saida, e.idproduto  
	FROM estoque e 
	where status = 'S'
    and idproduto = 1) saida 
)

