#!/bin/bash

## Autor: Lucas Vieira
## Alterado em: 15/01/2021

###### IMPORTANTE: ######
# Desenvolvido e Testado para Ubuntu 20.04 LTS



# Instala apps via apt-get
echo -e "Iniciando instalacao apps..."
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
wget -qO - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
#wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
#echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y python3-pip python3-venv sqlite3 sqlitebrowser \
	 libpq-dev python-dev apt-transport-https ca-certificates curl gnupg-agent software-properties-common \
	 git git-gui git-doc default-jre default-jdk dbeaver-ce google-chrome-stable
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get update && sudo apt-get install -y nodejs
sudo npm install -g aws-cdk
echo -e "\n\n# JDK" >> ~/.bashrc
echo -e "export JAVA_HOME=/usr/bin" >> ~/.bashrc
echo -e "export PATH=\$JAVA_HOME:\$PATH" >> ~/.bashrc
echo -e "\n\n# Alias: python/pip" >> ~/.bashrc
echo -e "alias python=/usr/bin/python3" >> ~/.bashrc
echo -e "alias pip=/usr/bin/pip3" >> ~/.bashrc
sudo snap install code --classic
source ~/.bashrc
echo -e "Apps instalados com sucesso!"


# Instala Docker-CE (engine, cli)
echo -e "Iniciando instalacao Docker-CE..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
#sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo apt-get update && sudo apt-get install -y docker-ce
sudo usermod -aG docker $USER
newgrp docker
echo -e "Docker-CE instalado e configurado com sucesso!"


# Instala Docker-Compose
echo -e "Iniciando instalacao Docker-Compose..."
curl -s https://api.github.com/repos/docker/compose/releases/latest \
	| grep browser_download_url \
	| grep docker-compose-Linux-x86_64 \
	| cut -d '"' -f 4 \
	| wget -qi -
sudo chmod +x docker-compose-Linux-x86_64
sudo mv docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
#sudo curl -L https://raw.githubusercontent.com/docker/compose/master/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
#source /etc/bash_completion.d/docker-compose
echo -e "Docker-Compose instalado e configurado com sucesso!"


# Instala JAVA
#echo -e "Iniciando instalacao JAVA..."
#sudo apt install openjdk-8-jdk
#wget -q https://public-aws-contatolucas.s3.amazonaws.com/downloads/jdk-8u201-linux-x64.tar.gz -P ~/
#tar -xvf ~/jdk-8u201-linux-x64.tar.gz
#sudo mv ~/jdk1.8.0_201 /opt/jdk
#rm jdk-8u201-linux-x64.tar.gz
#echo -e "\n\n#JDK" >> ~/.bashrc
#echo -e "export JAVA_HOME=/opt/jdk" >> ~/.bashrc
#echo -e "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc
#source ~/.bashrc
#echo -e "JAVA instalado e configurado com sucesso!"


# Instala Anaconda Python
#echo -e "Iniciando instalacao Anaconda Python..."
#wget -q https://public-aws-contatolucas.s3.amazonaws.com/downloads/Anaconda3-2019.07-Linux-x86_64.sh -P ~/
#wget -q https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -P ~/
#bash ~/Anaconda3-2019.10-Linux-x86_64.sh
#echo -e "alias python=~/anaconda3/bin/python3.7" >> ~/.bashrc
#source ~/.bashrc
#rm Anaconda3-2019.10-Linux-x86_64.sh
#echo -e "Anaconda Python instalado com sucesso!"


# Instala SPARK
echo -e "Iniciando instalacao SPARK..."
wget -q https://public-aws-contatolucas.s3.amazonaws.com/downloads/spark-2.4.4-bin-hadoop2.7.tgz -P ~/
tar -xvf ~/spark-2.4.4-bin-hadoop2.7.tgz
sudo mv ~/spark-2.4.4-bin-hadoop2.7 /opt/spark
rm spark-2.4.4-bin-hadoop2.7.tgz
echo -e "\n\n#SPARK" >> ~/.bashrc
echo -e "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo -e "export PATH=\$SPARK_HOME/bin:\$PATH" >> ~/.bashrc
echo -e "export PYSPARK_DRIVER_PYTHON=jupyter" >> ~/.bashrc
echo -e "export PYSPARK_DRIVER_PYTHON_OPTS=notebook" >> ~/.bashrc
source ~/.bashrc
echo -e "SPARK instalado e configurado com sucesso!"