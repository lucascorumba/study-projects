# Main
Este projeto herda muito do trabalho "covid-hospital".
Aqui iremos preparar e modelar dados das mesmas fontes para criação de um dashboard no Power BI.

Algumas diferenças importantes:
* Unificação de dados dos anos 2020, 2021 e 2022
* Informações sobre as unidades de atendimento serão disponibilizadas para análise
* Registros feitos por unidades de atendimento não registradas serão excluídos
* Implementação de um MER
* Em vez de um .ipynb, o processamento será automatizado com scripts .py 
* Toda visualização será feita no Power BI

Segue um pseudocódigo do planejamento até então:
1. Download dos arquivos contendo registros dos seguintes anos:
    * 2020, 2021 e 2022
2. Download dos dados referentes às unidades de atendimento
    * Criação de tabela fato "cnes"
3. Remoção de registros feitos por unidades de atendimento não mapeadas no item "2"
4. Processamento de dados sobre ocupação - limpeza e remoção de anomalias
    * Método aplicado no projeto "covid-hospital"
    * Atenção na implementação - o arquivo agora possui diversos anos
5. Conexão com Power BI
6. Junção dos registros restantes em uma única tabela fato "ocupação" utilizando Power Query
7. Esquematizar scripts .py para atualizar sob comando a base de dados carregada no Power BI

# Requisitos
É recomendado utilizar ambientes virtuais para instalação de pacotes requeridos pelo projeto.

Utilizando `venv`:
```
python -m venv venv-name

# Windows
venv-name\Scripts\activate.bat    # cmd
venv-name\Scripts\activate.ps1    # Power Shell

# Unix
source venv-name/bin/activate
```

*`pip>=23.2.1` para instalação via [PyPl](https://pypi.org/project/pandas/)*

```
pip install pandas
```