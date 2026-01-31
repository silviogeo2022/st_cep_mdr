# 📍 Visualizador de Localizações por CEP

Esta é uma aplicação web interativa desenvolvida em **Python** e **Streamlit** que permite visualizar endereços e coordenadas geográficas a partir de uma planilha Excel.

A aplicação conta com filtros dinâmicos (Bairro, Tipo e Logradouro) e exibe os resultados simultaneamente em uma tabela e em um mapa interativo.

## 📋 Funcionalidades

- **Filtros em Cascata:** Ao selecionar um Bairro, o filtro de Tipo se atualiza. Ao selecionar um Tipo, o filtro de Logradouro se atualiza.
- **Mapa Interativo:** Visualização dos pontos filtrados usando a biblioteca Folium.
- **Tabela de Dados:** Listagem dos endereços encontrados.
- **Compatibilidade Corporativa:** O código foi otimizado para rodar em ambientes com restrições de segurança (evitando erros de bloqueio de DLL/PyArrow).

## 🛠️ Pré-requisitos

- Python 3.8 ou superior instalado.
- VS Code (recomendado).

## 📂 Estrutura de Arquivos

Certifique-se de que sua pasta contenha os seguintes arquivos:

- `app.py`: O código principal da aplicação.
- `dataset.xlsx`: O arquivo Excel com os dados.
- `logo.png`: A imagem da logomarca.
- `requirements.txt`: Lista de dependências.

## 📊 Estrutura do Excel (`dataset.xlsx`)

Para que a aplicação funcione corretamente, o arquivo Excel deve conter as seguintes colunas (exatamente com estes nomes):

| Coluna      | Descrição                          |
| :---------- | :--------------------------------- |
| `CEP`       | O código postal.                   |
| `Tipo`      | Tipo do logradouro (Rua, Av, etc). |
| `Logradouro`| Nome da rua/avenida.               |
| `Bairro`    | Nome do bairro.                    |
| `Latitude`  | Coordenada decimal (ex: -2.04587). |
| `Longitude` | Coordenada decimal (ex: -47.5522). |

> **Nota:** Certifique-se de que a Latitude e Longitude usem **ponto** (.) como separador decimal, e não vírgula.

## 🚀 Instalação e Execução

1. **Abra o terminal** na pasta do projeto.

2. **Instale as dependências** executando o comando:
   ```bash
   pip install -r requirements.txt
