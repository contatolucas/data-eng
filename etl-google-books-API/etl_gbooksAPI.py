import requests
import json
import pandas as pd
import numpy as np
import awswrangler as wr
import boto3
from datetime import datetime


#seta chaves de acesso na AWS
ACCESS_KEY = 'XXXXXXXXXXXXXXXXX' # ACCESS_KEY unica por usuario (config em IAM Management Console na AWS)
SECRET_KEY = 'xxXXxxXXxxXXXXxXXXxXXxxxxXXXXX' # SECRET_KEY unica por usuario (config em IAM Management Console na AWS)

# seta session na AWS
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

#bucket do S3 (IMPORTANTE: criar o bucket via Console na AWS ou via AWS CLI)
bucket = 'data-lake-gbooks'

# seta engine do banco de dados (IMPORTANTE: criar a instancia via Console na AWS ou via AWS CLI)
# consultar o arquivo 'config_inicial_db.sql'
postgres_engine = wr.db.get_engine(
    db_type="postgresql",
    host="xxxxxxx.xxxxxxxxx.us-east-1.rds.amazonaws.com",
    port=5432,
    database="db_gbooks",
    user="usuario",
    password="senha"
)

# define variavel com o termo de busca
# consultar documentacao GBooks API, na sessao: https://developers.google.com/books/docs/v1/using#query-params
pesquisa = 'inpublisher:Saraiva+Educação'

# class com as instrucoes de extracao da API do Google Books (formato json paginado)
class extrair_gbooks_API():
    
    def __init__(self):
        self.g_API_key = 'xxXXxxXXxxXXXXxXXXxXXxxxxXXXXX' # Criar API Key na pag de APIs do Google
        self.max_res = 40
    
    # funcao para extracao dos dados - json retorna no max 40 volumes/livros por requisao
    def busca(self, value):
        par_total = {'q':value, 'key':self.g_API_key}
        r_total = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=par_total)
        rjson_total = r_total.json()
        var_Total = rjson_total['totalItems']        
        index_ini = 0
        count_reg = 0
        
        df = pd.DataFrame()
        
        # loop armazena em df temporario os livros (de 40 em 40), ate atingir o total de livros (vide variavel 'var_Total')
        while (count_reg < var_Total):
            parms = {'q':value, 'maxResults':self.max_res, 'startIndex':index_ini, 'key':self.g_API_key}
            r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
            rjson = r.json()
            try:
                reg = rjson["items"]
            except:
                break
            else:
                df_temp = pd.json_normalize(reg)
                df = pd.concat([df, df_temp], ignore_index=True)
                df.reset_index()

                index_ini = df.sort_index(ascending=False).head(1).index.values[0] + 1
                count_reg = len(df.index)
            
        return df

#instancia a class 'extrair_gbooksAP'
livros = extrair_gbooks_API()


# Cria base raw

# atribui o DataFrame de retorno da class/def em objeto para realizacao de ETL/ELT
df_raw = livros.busca(pesquisa)

# exporta base com o resultado final bruto para consumo posterior, caso necessario (raw_data no Data Lake)
agora_raw = datetime.now().strftime("%Y%m%d%H%M%S")
bucket_raw = f"s3://{bucket}/raw_data/gbooks_raw_Saraiva_Educacao_{agora_raw}.csv"
wr.s3.to_csv(df_raw, bucket_raw, header=True, sep='|', index=False , encoding='utf-8', boto3_session=session)


# ::. ETL Google Books .::

# Cria base standard

# cria campo Isbn13
df_type_isbn = (
    df_raw["volumeInfo.industryIdentifiers"]
    .apply(pd.Series)
    .rename(columns={0: "campo1", 1:"campo2"})
)
df_type_isbn_temp1 = (
    df_type_isbn['campo1']
    .apply(pd.Series)
)
df_type_isbn_temp2 = (
    df_type_isbn['campo2']
    .apply(pd.Series)
)
df_type_isbn_temp1['campo2Type'] = df_type_isbn_temp2[['type']]
df_type_isbn_temp1['campo2Identifier'] = df_type_isbn_temp2[['identifier']]
df_type_isbn_temp1.loc[df_type_isbn_temp1['type'] == 'ISBN_10', ['identifier']] = df_type_isbn_temp1['campo2Identifier']
df_type_isbn_temp1.loc[df_type_isbn_temp1['type'] == 'ISBN_10', ['type']] = df_type_isbn_temp1['campo2Type']
df_type_isbn_temp1.loc[df_type_isbn_temp1['type'] == 'OTHER', ['identifier']] = np.nan
df_type_isbn_final = df_type_isbn_temp1[['identifier']]
df_raw['Isbn13'] = df_type_isbn_final[['identifier']]

# padrozina com S/N campos booleanos (True/False)
df_raw['saleInfo.isEbook'] = np.where(df_raw['saleInfo.isEbook'], 'S', 'N')
df_raw['accessInfo.publicDomain'] = np.where(df_raw['accessInfo.publicDomain'], 'S', 'N')
df_raw['accessInfo.epub.isAvailable'] = np.where(df_raw['accessInfo.epub.isAvailable'], 'S', 'N')
df_raw['accessInfo.pdf.isAvailable'] = np.where(df_raw['accessInfo.pdf.isAvailable'], 'S', 'N')

# padroniza campo substituindo FOR_SALE/NOT_FOR_SALE para A_VENDA/NAO_A_VENDA
df_raw['saleInfo.saleability'].replace('FOR_SALE', 'A_VENDA', inplace=True)
df_raw['saleInfo.saleability'].replace('NOT_FOR_SALE', 'NAO_A_VENDA', inplace=True)

# converte campo em datetime (valor nulos = NaT e padroniza datas que possuem somente o ano)
df_raw['volumeInfo.publishedDate'] = pd.to_datetime(df_raw['volumeInfo.publishedDate'], errors='coerce')

# cria campo 'anoPublicacao' baseado no em 'volumeInfo.publishedDate'
df_raw['anoPublicacao'] = df_raw['volumeInfo.publishedDate'].dt.year.astype('object')

# lista de campos da base standard
df_list_standard = [
    'id',
    'volumeInfo.title',
    'volumeInfo.subtitle',
    'volumeInfo.authors',
    'volumeInfo.publisher',
    'volumeInfo.publishedDate',
    'volumeInfo.description',
    'volumeInfo.pageCount',
    'volumeInfo.categories',
    'volumeInfo.language',
    'volumeInfo.canonicalVolumeLink',
    'saleInfo.country',
    'saleInfo.saleability',
    'saleInfo.listPrice.currencyCode',
    'saleInfo.isEbook',
    'saleInfo.listPrice.amount',
    'accessInfo.publicDomain',
    'accessInfo.epub.isAvailable',
    'accessInfo.pdf.isAvailable',
    'volumeInfo.averageRating',
    'anoPublicacao',
    'Isbn13'
]

# cria DataFrame da base standard: campos da base bruta tratadas e feita selecao previa de campos para utilizacao/estudo
df_standard = df_raw[df_list_standard]

# exporta base com o resultado standard para consumo posterior, caso necessario (standard_data no Data Lake)
agora_standard = datetime.now().strftime("%Y%m%d%H%M%S")
bucket_standard = f"s3://{bucket}/standard_data/gbooks_standard_Saraiva_Educacao_{agora_standard}.csv"
wr.s3.to_csv(df_standard, bucket_standard, header=True, sep='|', index=False , encoding='utf-8', boto3_session=session)


# Cria base curated

# dicionario com a lista de colunas vindas do df_standard renomeando para visao negocio (selecao das principais colunas)
df_list_curated = {'id':'id_livro',
'volumeInfo.title':'titulo',
'volumeInfo.subtitle':'subtitulo',
'Isbn13':'isbn13',
'volumeInfo.authors':'autor',
'volumeInfo.publishedDate':'data_publicacao',
'anoPublicacao':'ano_publicacao',
'volumeInfo.pageCount':'numero_paginas',
'saleInfo.saleability':'disponivel_venda',
'saleInfo.listPrice.currencyCode':'moeda_preco',
'saleInfo.listPrice.amount':'preco',
'volumeInfo.language':'linguagem',
'volumeInfo.categories':'categoria', 
'volumeInfo.publisher':'editora',
'volumeInfo.canonicalVolumeLink':'link_livro',
'accessInfo.epub.isAvailable':'disponivel_epub',
'accessInfo.pdf.isAvailable':'disponivel_pdf',
'accessInfo.publicDomain':'dominio_publico'
}

# cria DataFrame da base curated: feita selecao somente dos campos importantes para negocio
df_curated = df_standard[df_list_curated.keys()].copy()
df_curated.rename(columns=df_list_curated, inplace=True)

# padroniza substituindo A_VENDA/NAO_A_VENDA para S/N
df_curated['disponivel_venda'].replace('A_VENDA', 'S', inplace=True)
df_curated['disponivel_venda'].replace('NAO_A_VENDA', 'N', inplace=True)

# normaliza campo 'autor' (separando por ',' quando existe mais de um autor) e demais tratamentos
df_curated['autor'] = df_curated.autor.str.join(",")
df_curated['autor'] = df_curated['autor'].str.replace(' e ',', ')
df_curated['autor'] = df_curated['autor'].str.replace(' / ',', ')
df_curated['autor'] = df_curated['autor'].str.replace('/ ',', ')
df_curated['autor'] = df_curated['autor'].str.replace(' /',', ')
df_curated['autor'] = df_curated['autor'].str.replace(',',', ')

# normaliza campo 'categoria' (separando por ',' quando existe mais de uma categoria) e demais tratamentos
df_curated['categoria'] = df_curated.categoria.str.join(",")
df_curated['categoria'] = df_curated['categoria'].str.replace(' & ',', ')
df_curated['categoria'] = df_curated['categoria'].str.replace(' / ',', ')

# normaliza CASE SENSITIVE (MAIUSCULO)
df_curated['titulo'] = df_curated['titulo'].str.upper()
df_curated['autor'] = df_curated['autor'].str.upper()
df_curated['categoria'] = df_curated['categoria'].str.upper()

# cria campo com data/hora da carga
df_curated['data_carga'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# exporta base com o resultado curated para area de negocio (via Data Lake curated_data OU via DB)
agora_curated = datetime.now().strftime("%Y%m%d%H%M%S")
bucket_curated = f"s3://{bucket}/curated_data/gbooks_curated_Saraiva_Educacao_{agora_curated}.csv"
wr.s3.to_csv(df_curated, bucket_curated, header=True, sep='|', index=False , encoding='utf-8', boto3_session=session)

# cria a tabela 'tb_gbooks_curated' fazendo insert na mesma com os dados do 'df_curated'
wr.db.to_sql(df_curated, postgres_engine, schema="public", name="tb_gbooks_curated", if_exists="replace", index=False)