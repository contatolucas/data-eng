CREATE TABLE tb_gbooks_aggregated AS (
SELECT ano_publicacao, categoria, disponivel_venda, disponivel_epub, disponivel_pdf,
sum(numero_paginas) as soma_numero_paginas, avg(numero_paginas) as media_numero_paginas,
sum(preco) as soma_preco, avg(preco) as media_preco 
FROM db_gbooks.public.tb_gbooks_curated
GROUP BY ano_publicacao, categoria, disponivel_venda, disponivel_epub, disponivel_pdf
);