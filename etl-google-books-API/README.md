# EXTRAÇÃO E CARGA DE DADOS DE LIVROS - GOOGLE BOOKS API

Processo de extração, tratamento e carga de volumes (livros) dO **[Google Books API](https://developers.google.com/books)**.

O processo apresentado aqui trata a extração de livros conforme termo/condições de pesquisa (**[Mais detalhes aqui](https://developers.google.com/books/docs/v1/using#query-params)**).

#### Antes de começar:
- Requisitos:
    - Python 3.7+ (preferencialmente instalar a distribuição Anaconda Python 4.7+)
        - awswrangler
        - boto3
- Criar uma conta na AWS (caso ainda não tenha): https://aws.amazon.com/pt/;
- Definir chaves de acesso no IAM Management na AWS (`ACCESS_KEY` e `SECRET_KEY`) e setar nas respectivas variáveis do arquivo **[etl_gbooksAPI](https://github.com/contatolucas/data-eng/blob/master/etl-google-books-API/etl_gbooksAPI.py)**;
- Criar um bucket no AWS S3 que será o Data Lake do projeto e setar na variável `bucket` do arquivo **[etl_gbooksAPI](https://github.com/contatolucas/data-eng/blob/master/etl-google-books-API/etl_gbooksAPI.py)**;
- Criar uma instância PostgreSQL no AWS RDS (que permita conexão pública) que será o Banco de Dados/Data Mart do projeto e setar as configurações em `postgres_engine` do arquivo **[etl_gbooksAPI](https://github.com/contatolucas/data-eng/blob/master/etl-google-books-API/etl_gbooksAPI.py)**;
- Criar uma API Key (**[Criar chave de API](https://cloud.google.com/docs/authentication/api-keys?visit_id=637403001827530704-1456085297&rd=1#creating_an_api_key)**) <br>
*os recursos da AWS utilizados aqui, contemplam o nível gratuito


#### Iniciando
Após definir e configurar os recursos acima na AWS, abra um client de Banco de Dados (DBeaver, pgAdmin, por exemplo), configure a conexão de acesso a instância PostgreSQL no RDS e rode as queries a seguir (também disponíveis no arquivo **[etl_gbooksAPI](https://github.com/contatolucas/data-eng/blob/master/etl-google-books-API/etl_gbooksAPI.py)**):
```sql
-- cria usuario/role e atribui acesso admin ao mesmo
CREATE ROLE user_etl WITH PASSWORD 'etl@2020' CREATEDB CREATEROLE LOGIN;
GRANT rds_superuser TO user_etl;

-- cria o banco 'db_gbooks' utilizado no processo de ETL/ELT
CREATE DATABASE db_gbooks OWNER user_etl TABLESPACE default;
```

### Executar ETL/ELT
O arquivo principal do projeto **[etl_gbooksAPI](https://github.com/contatolucas/data-eng/blob/master/etl-google-books-API/etl_gbooksAPI.py)** executará todo o processo de ETL/ELT consumindo os dados da API do Google Books, tratamento e carga no Data Lake (bucket do S3) e no Bando de Dados/Data Mart (PostreSQL no RDS). <br>
Principais pontos do arquivo:
- setar a condição/termo de busca na API em:
```py3
pesquisa = 'inpublisher:Saraiva+Educação'
```
- consumo dos volumes (livros) da API pela classe `extrair_gbooksAPI()` com retorno em JSON paginado (40 em 40 volumes) guardando o resultado (em loop) em pandas `DataFrame` para utilização posterior durante a execução; <br><br>
- após a extração completa conforme a condição/termo buscado, são iniciados os processos de transformações e cargas:
    - no Data Lake são armazenados as etapas de transformação comumente utilizadas - raw data, standard data e curated data - onde temos os dados brutos (sem qualquer tratamento prévio), padronização inicial dos dados (como tipo de dados, normalização de dados nos campos, etc) e curadoria final dos dados (mais normalização e seleção dos dados visando a utilização pela área de negócio), respectivamente;
    - no Banco de Dados/Data Mart é armanezado somente os dados já curados (curated data do Data Lake) para consumo em ferramentas de visualização (Power BI, Tableau, Metabase, etc) ou para utilização em ferramentas de Ciência de Dados (como Jupyter Notebook, Google Colab, etc) <br><br>
    
Para executar o arquivo, abra o Shell/CMD e navegue até a pasta do projeto (caso ainda não esteja):
```sh
$ python etl_gbooksAPI.py
```
