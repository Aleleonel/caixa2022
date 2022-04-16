select 
	idproduto, 
    p.descricao, 
    coalesce(
		(SELECT 
			sum(e.estoque) entrada 
		 FROM estoque e 		
		 where status = 'E' 
		 and e.idproduto = i.idproduto), 0) entrada,  
	coalesce(
		(SELECT 
			sum(e.estoque) saida
		 FROM estoque e 
		 where status = 'S'
		 and e.idproduto = i.idproduto), 0) saida,  
     
      coalesce(
		  ((SELECT 
			 sum(e.estoque) entrada 
		   FROM estoque e 		
		   where status = 'E' 
		   and e.idproduto = i.idproduto) -  
		  (SELECT 
			 sum(e.estoque) saida
		   FROM estoque e 
		   where status = 'S'
		   and e.idproduto = i.idproduto)), 0) estoque

from 
	estoque i
inner join produtos p on p.codigo = i.idproduto    
group by 
	idproduto
	

