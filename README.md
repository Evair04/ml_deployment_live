## Descrição geral do projeto ML Deployment

Este projeto visa realizar a implantação de um modelo de ML em produção, ou seja, em um servidor dedicado que poderá responder solicitações de usuários na internet por meio de um web browser.

## Passos para a criação e execução deste projeto

### Criar um ambiente virtual

```commandline
python3 -m venv venv
```

### Ativar o ambiente virtual
```commandline
source venv/bin/activate
```

### Instalar o Streamlit
```commandline
pip install streamlit
```

### Testar o Streamlit
```commandline
streamlit hello
```
ou
```commandline
python -m streamlit hello
```

### Rodar o App
```commandline
streamlit run app.py
```

## Salvar e carregar as libs dentro do ambiente virtual

### Salvar as libs
```commandline
pip freeze > requirements.txt
```

### Instalar todas as libs
```commandline
pip install -r requirements.txt
```


## Configurar AWS
```commandline
sudo apt update
```

```commandline
sudo apt-get update
```

```commandline
sudo apt upgrade -y
```

```commandline
sudo apt install python3-pip
```

```commandline
sudo apt install python3.10-venv
```

## Para deixar o sistema rodando, usar screen (console virtual)
https://www.gnu.org/software/screen/manual/screen.html

```commandline
screen -S streamlit_session
```

### Para sair do console virtual
```commandline
ctrl+a d
```

### Para entrar novamente no console virtual
```commandline
screen -r streamlit_session
```

### Para visualizar os consoles virtuais rodando
```commandline
screen -ls
```

### Para matar o console virtual
```commandline
screen -X -S streamlit_session quit
```
