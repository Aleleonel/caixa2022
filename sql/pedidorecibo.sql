select 
	p.codigo, 
    p.descricao, 
    coalesce(    
		(SELECT 			
			sum(e.valor_total)
		 FROM pedidocaixa e 		
		 where nr_caixa = 249), 0) total,
         
	coalesce(
         (SELECT 			
				sum(e.quantidade)  
		 FROM pedidocaixa e 		
		 where nr_caixa = 249), 0) quantidade

from 
	produtos p
inner join pedidocaixa e on p.codigo = e.cod_produto
and nr_caixa = 249
group by 
	e.cod_produto
    
    
  

	
	