# PROCESSO ETL (E T L) - GOOGLE BOOKS API

Processo de extração, tratamento e carga de volumes (livros) da **[Google Books API](https://developers.google.com/books)**.

O processo apresentado aqui trata a extração de livros conforme termo/condições de pesquisa (**[Mais detalhes aqui](https://developers.google.com/books/docs/v1/using#query-params)**).

Link dos dados abertos do Governo do Brasil: http://dados.gov.br/dataset/microdados-prova-brasil 

#### Antes de começar:
- Criar uma conta na AWS (caso ainda não tenha): https://aws.amazon.com/pt/;
- Definir chaves de acesso no IAM Management na AWS (`ACCESS_KEY` e `SECRET_KEY`) e setar nas respectivas variáveis do arquivo **[arquivoPY](http://)**;
- Criar um bucket no AWS S3 e setar na variável `bucket` do arquivo **[arquivoPY](http://)**;
- Criar uma instância PostgreSQL no AWS RDS (que permita conexão pública) para setar as configurações em `postgres_engine` do arquivo **[arquivoPY](http://)**;
- Criar uma API Key (**[Criar chave de API](https://cloud.google.com/docs/authentication/api-keys?visit_id=637403001827530704-1456085297&rd=1#creating_an_api_key)**)
*os recursos da AWS utilizados aqui, contemplam o nível gratuito


#### Iniciando
Após definir e configurar os recursos acima na AWS, abra um client de Banco de Dados (DBeaver, pgAdmin, por exemplo), configure a conexão de acesso a instância PostgreSQL no RDS e rode as queryes a seguir (também disponíveis no arquivo **[arquivoSQL](http://)**):
```sql
-- cria usuario/role e atribui acesso admin ao mesmo
CREATE ROLE user_etl WITH PASSWORD 'etl@2020' CREATEDB CREATEROLE LOGIN;
GRANT rds_superuser TO user_etl;

-- cria o banco 'db_gbooks' utilizado no processo de ETL/ELT
CREATE DATABASE db_gbooks OWNER user_etl TABLESPACE default;
```


O Airflow foi escolhido para orquestrar a pipeline de dados por ser flexível e permitir organizar os passos com facilidades, caso necessite de escolabilidade pode facilmente incoporar outros frameworks de processamento distribuido. 
O Redshift é totalmente gerenciado e oferece uma solução completa para montar o DataWarehouse. 
O S3 permite armazenar os dados e carregar através dele as tabelas do Redshift, se tornando uma stagging area.
E o Metabase é uma solução de visualização de dados open source com recursos fáceis e eficientes para montar dashboards.
    
### Modelagem Dimensional dos dados

![alt text](https://github.com/cicerojmm/analiseDadosAbertosProvaBrasil/blob/master/images/modelagem-dimensional.png?raw=true)

### Execução do Projeto
O projeto está totalmente baseado no Docker e Docker Compose, basta seguir os passos abaixo:
1. Executar imagem do Airflow: 
```sh
$ docker-compose -f docker-compose-airflow.yml up -d
```
2. Executar imagem do Metabase: 
```sh
$ docker-compose -f docker-compose-metabase.yml up -d
```
2. Baixar os dados abertos: 
```sh
$ ./baixar_dados_abertos.sh
```
3. No painel web do Airflow cadastrar as connections do S3 com o nome *aws_s3* e do Redshift com o nome *aws_redshift*.
4. Criar as tabelas necessárias no Redshift utilizando o script *criacao-tabelas-dw-redshift.sql* deste repositório.
5. Criar um bucket no S3 e alterar o nome do bucket no código para o criado neste passo.
5. Executar a pipeline de dados no airflow.
6. Configurar e criar as visualizações no Metabase.

### Fluxo Completo no Airflow
![alt text](https://github.com/cicerojmm/analiseDadosAbertosProvaBrasil/blob/master/images/pipeline-completa-airflow.png?raw=true)

### Dashboard gerado no Metabase
![alt text](https://github.com/cicerojmm/analiseDadosAbertosProvaBrasil/blob/master/images/dashboard-metabase.png?raw=true)
