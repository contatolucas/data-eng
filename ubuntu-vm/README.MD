## >> Rodar shell script (instala apps, Anaconda/Python, Java, Spark...)
	bash config_python_ubuntu.sh

## >> Incluir no .bashrc (remove "(base)" do terminal, após instalação Anaconda)
	PS1="$(echo $PS1 | sed 's/(base) //') "
	
	# compilar/ativar modificações no .bashrc
	source ~/.bashrc
