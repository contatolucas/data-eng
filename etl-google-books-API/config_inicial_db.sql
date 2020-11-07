-- rodar com o usuario inicial definido na criacao da instancia no AWS RDS
CREATE ROLE user_etl WITH PASSWORD 'etl@2020' CREATEDB CREATEROLE LOGIN;
GRANT rds_superuser TO user_etl;

CREATE DATABASE db_gbooks OWNER user_etl TABLESPACE default;