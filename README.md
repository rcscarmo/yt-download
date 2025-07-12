# Mp3 Download
Script que pesquisa e abaixa musicas do youtube a partir de um arquivo


# Instrucoes
- Instale o software `FFMPEG` em seu sistemas [Download do FFMPEG](https://ffmpeg.org/download.html)
- Crie um ambiente de desenvolvimento ```python -m venv .venv```
- Ative o ambiente
##### Windows
```.venv/Scripts/activate```

##### Linux
```source .venv/bin/activate```

- Instale as dependencias do python com o comando `pip install -r requirements.txt`
- Coloque o nome das musicas dentro da pasta `listas` nomeando o arquivo da forma que preferir ex.: ```paula-fernandes.txt```, ```bruna-karla.txt```, ```xuxa.txt```
- Renomei o arquivo `config-default.json` para `config.json` e coloque sua chave da api do youtube no local indicado
- Execute o script `main.py`
- Aguarde o download
- Sera criado uma pasta com o nome escolhido do arquivo dentro da pasta `saida` com as musicas baixardas

# Informacoes extras:
- O custo de pesquisa do youtube por chave de api eh de 100 pontos
o plano gratuito concede 10.000 ( Dez mil ) pontos gratuitos diariamente, tenha isso em mente.
- Eh possivel contonar essa situacao criando novos projetos, criando uma chave api nesse projeto e
adicionando ```Youtube Data API V3``` nesse projeto

# Contribuicoes
- Faca o fork do projeto
- Crie uma branch com a sua contribuicao ```git branch -b minha-contribuicao```
- Faca o pull request do commit da contribuicao

