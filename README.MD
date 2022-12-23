# PROJECT NAME : PDV-Crontrol
 / * Um sistemas de venda com cadastro de clientes, produtos e controle de estoque * /

 # HOW TO RUN THIS PROJECT

 - ESTE PROJETO RODA EM VERSÕES 
     - Python Ver 3.X 
     - PyQt5  Ver 5.15.4
     - mysql  Ver 8.0.29
     - mysql-connector-python Ver 8.0.23
 
 - INSTALE AS DEPENDENCIAS DE FORMA GLOBAL EM SUA MAQUINA COM:
    - pip install -r requirements.txt
    
 - IMPORTE O BANCO DE DADOS
 - USUÁRIO adm senha 1

# HOW TO DO

    echo "# caixa" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin git@github.com:Aleleonel/caixa.git
    git push -u origin main
    
# Objetivo do projeto

	- Sistema de Controle de Estoque
	- Sistema de Controle de Caixa (pdv)

	- Sistema de Geração de Nota Fiscal
    - Sistema de Controle Financeiro

	- Sistema de Cadastro de Produtos
	
	- Sistema de Controle de Compra e Venda
	- Sistema de Relatório de Receitas Brutas
    
	- Sistema de Gestão de Documentos
	- Sistema de Calendário e Agendamento

# issues

 - QUANDO ESCOLHEMOS IMPRIMIR O CUPOM O PROGRAMA FECHA PARA ABRIR A CADA DE IMPRESSÃO E DEPOIS QUE IMPRIMIMOS EME ABRE NOVAMENTE. DESABILITEI A IMPRESSÃO, TEMPORARIAMENTE. POR ENQUANTO APENAS UM ARQUIVO EM FORMATO PDF É GERADO ATE EU PENSAR EM UMA SOLUÇÃO MELHOR QUE IMPRESSÃO EM A4, CERTAMENTE UMA IMPRESSÃO DE CUPOM SERÁ MELHOR.

 - QUANDO DELETAMOS UM OU MAIS CLIENTES PRECISAMOS REINICIAR/ ATUALIZAR FRONT-CAIXA, CASO CONTRARIO O PROGRAMA DARÁ ERRO. A IDEIA É NÃO PODER DELETAR, MAS DESATIVAR CLIENTES E PRODUTOS, MANTENDO UM HISTÓRICO DE SAIDAS E COMPRAS.

 # RELACIONADO

 - INSERIR OS PRODUTOS PELO NUMERO DO CÓDIGO OU PELA DESCRIÇÃO.
 - CRIAR UMA TABELA PARA CADASTRAR UNIDADE DE MEDIDA
 - MODIFICAR CONSULTA DE CLIENTES
 - MODIFICAR CADASTRO ESTOQUE
 - EDIÇÃO DE ITENS E CLINTES NA TELA DE CADASTRO.
 - EM CONTROLE DE PRODUTO PRECISAMOS PODER EDITAR O VALOR DO PRODUTO SUA DESCRIÇÃO E UNIDADE.

 
