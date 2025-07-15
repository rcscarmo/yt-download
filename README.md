# Mp3 Download
Script que pesquisa e abaixa músicas do YouTube a partir de um arquivo.


# Instruções
- Instale o software `FFMPEG` em seu sistemas [Download do FFMPEG](https://ffmpeg.org/download.html)
- Crie um ambiente de desenvolvimento ```python -m venv .venv```
- Ative o ambiente
##### Windows
```.venv/Scripts/activate```

##### Linux
```source .venv/bin/activate```

- Instale as dependências do Python com o comando `pip install -r requirements.txt`
- Coloque o nome das músicas dentro da pasta `listas` nomeando o arquivo da forma que preferir, ex.: ```paula-fernandes.txt```, ```bruna-karla.txt```, ```xuxa.txt```
- Renomeei o arquivo `config-default.json` para `config.json` e coloque suas chaves da API do YouTube no local indicado ```["CHAVE 1", "CHAVE 2", "CHAVE 3"]```
- Execute o script `main.py`
- Aguarde o download
- Será criada uma pasta com o nome escolhido do arquivo dentro da pasta `saida` com as músicas baixadas

# Informações extras:
- O custo de pesquisa do YouTube por chave de API é de 100 pontos. O plano gratuito concede 10.000 (Dez mil) pontos gratuitos diariamente, tenha isso em mente.
- É possível contornar essa situação criando novos projetos, criando uma chave API nesse projeto e adicionando ```Youtube Data API V3``` nesse projeto.

# Contribuições
- Faça o fork do projeto
- Crie uma branch com a sua contribuição ```git branch -b minha-contribuicao```
- Faça o pull request do commit da contribuição

