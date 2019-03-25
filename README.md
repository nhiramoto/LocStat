# LocStat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/nhtoshiaki/LocStat.svg?branch=master)](https://travis-ci.org/nhtoshiaki/LocStat)

LocStat é um Web Scraper responsável por analisar repositórios públicos hospedados no Github e criar relatórios com a estatística de Linhas de Código (LOC - Lines Of Code) para cada tipo de arquivo.

## Requisitos

Para utilizar este projeto os seguintes programas devem estar instalados:

- Python (Testado na versão 3.7)
- Pipenv

Caso não tenha o Pipenv, para instalá-lo basta executar o pip:

```sh
pip install pipenv
```

> O comando anterior deve ser executado com elevação de privilégio, aplique de acordo com o sistema utilizado.

## Instalação

Antes de executar o projeto:

- Clone o repositório:

```sh
git clone https://github.com/nhtoshiaki/LocStat.git LocStat
cd LocStat
```

- Instale as dependências:

```sh
pipenv install
```

## Como usar

Este programa lê a lista de repositórios de um arquivo chamado `repositories.txt` que deve estar no diretório raiz do projeto. Cada linha do `repositories.txt` deve conter a referência de um repositório no Github no formato `user_name/repository_name`. Caso a linha comece com o símbolo `#` o repositório é descartado. Por exemplo, se o arquivo conter:

```
django/django
# d3/d3
scrapy/scrapy
```

somente os repositórios [`django/django`](https://github.com/django/django) e [`scrapy/scrapy`](https://github.com/scrapy/scrapy) serão analisados.

Para executar o projeto basta executar:

```sh
pipenv run project
```

Após executar o projeto, para cada repositório listado no `repositories.txt` o programa cria um arquivo renomeado no formato `user_name-repository_name.txt` com as seguintes informações:

- Referência do repositório (`user_name/repository_name`)
- Quantidade total de linhas
- Quantidade total de bytes
- Tabela com a quantidade e porcentagem de linhas e bytes para cada tipo de arquivo
- Estrutura da árvore de arquivos do projeto

## Configurando o crawler

As configurações do crawler estão contidos no arquivo [`settings.py`](https://github.com/nhtoshiaki/LocStat/blob/master/LocStat/settings.py), neste arquivo podem ser alterados por exemplo o user-agent e o delay dos requests configurados para o crawler.

## Testes

O projeto inclui alguns testes, para executá-los:

```sh
pipenv run tests
```

## Implementado com

- [Scrapy](https://scrapy.org/)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](https://github.com/nhtoshiaki/LocStat/blob/master/LICENSE) para mais detalhes.