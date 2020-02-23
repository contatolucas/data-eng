## Arquivos para criação de imagem do Docker:

  - Dockerfile: arquivo com as configurações para criação da imagem;
  - pip_list.txt: arquivo com pacotes python para serem instalado via pip na criação da imagem

## Exemplo de comador Docker para criar a imagem:

  docker build . -t linux-ds
  
## Exemplo de como rodar um container Docker sob a imagem criada:

  docker run -it linux-ds