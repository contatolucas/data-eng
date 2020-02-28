FROM continuumio/anaconda3:latest

ENV PATH /opt/jdk/bin:/opt/spark/bin:$PATH
ENV JAVA_HOME /opt/jdk
ENV SPARK_HOME /opt/spark
ENV PYSPARK_DRIVER_PYTHON jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS notebook

WORKDIR /

# Instala apps complementares
RUN apt-get update && apt-get install -y vim sqlite3 sqlitebrowser

# Copia e instala pacotes Python adicionais
COPY pip_list.txt ./
RUN /opt/conda/bin/pip install -r pip_list.txt && rm pip_list.txt

# Baixa e instala JAVA (JDK)
RUN wget -q https://public-aws-contatolucas.s3.amazonaws.com/downloads/jdk-8u201-linux-x64.tar.gz && \
	tar -xvf jdk-8u201-linux-x64.tar.gz && \
	mv jdk1.8.0_201 /opt/jdk && \
	rm jdk-8u201-linux-x64.tar.gz

# Baixa e instala Spark
RUN wget -q https://public-aws-contatolucas.s3.amazonaws.com/downloads/spark-2.4.4-bin-hadoop2.7.tgz && \
	tar -xvf spark-2.4.4-bin-hadoop2.7.tgz && \
	mv spark-2.4.4-bin-hadoop2.7 /opt/spark && \
	rm spark-2.4.4-bin-hadoop2.7.tgz