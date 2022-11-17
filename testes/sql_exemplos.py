# select que pega todos os pedidos
comando_sql = """ SELECT
                    nr_caixa,
                    cod_produto,
                    p.descricao,
                    quantidade,
                    valor_total,
                    ultupdate
                FROM
                    pedidocaixa
                LEFT JOIN produtos as p ON cod_produto = p.codigo
                order by
                    ultupdate desc
            """
