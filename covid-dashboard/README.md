# Main
Este projeto herda muito do trabalho [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital).
Aqui iremos preparar e modelar dados das mesmas fontes para criação de um dashboard no Power BI.

Algumas diferenças importantes:
* Unificação de dados dos anos 2020, 2021 e 2022 (ainda não há dados de 2023 em diante nesta fonte)
* Informações sobre as unidades de atendimento serão disponibilizadas para análise
* Informações sobre a localização de cada unidade de saúde registrada
* Registros feitos por unidades de atendimento não registradas serão excluídos
* Implementação de um MER
* Em vez de um .ipynb, o processamento será automatizado com scripts .py 
* Toda visualização será feita com Power BI

# Cronograma:
- [x] Download dos arquivos contendo registros dos seguintes anos:
    * 2020, 2021 e 2022
- [x] Download dos dados referentes às unidades de atendimento
    * Criação de tabela dimensão "cnes"
- [x] Remoção de registros feitos por unidades de atendimento não mapeadas na tebela dimensão
- [x] Processamento de dados sobre ocupação - limpeza e remoção de anomalias
    * Método aplicado no projeto "covid-hospital"
    * Atenção na implementação - o arquivo agora possui diversos anos
    * unificação dos dados para criação da tabela fato "ocupação"
- [x] Conexão com Power BI
- [x] Implementação de scripts para automatização da limpeza e unificação de registros na base de dados
- [x] Modelagem de dados
- [x] Criação de medidas com DAX
- [x] Construção dos visuais no dashboard
- [x] Gravação da demonstração do processamento de dados
- [ ] Gravação da demonstração do dashboard finalizado
- [ ] Finalização do README.md

# Processamento
Com os dados brutos obtidos, os scripts realizam o processamento, limpeza e unificação dos dados.
Primeiro preparamos o arquivo que será base para a tabela dimensão de leitos:
![execução do processo de limpeza e unificação da tabela dimensão](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/record-lookup.gif?raw=true)

Em seguida fazemos o mesmo com a os arquivos base para a tabela fato de ocupação hospitalar:
![execução do processo de limpeza e unificação da tabela fato](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/record-fact.gif?raw=true)

Ao executar arquivo `main.py` podemos escolher qual operação realizar. Passando o parâmetro `lookup` realizamos o processamento de arquivos relaciocados à leitos. Com o parâmetro `fact` fazemos o processo adaptado do projeto [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital).
Em ambas situações os próximos parâmetros na linha de comando são arquivos `.csv`. Aqui usamos dos anos 2020, 2021 e 2022 já que são os disponíveis. Mas, caso haja atualização, os scripts realizam o mesmo procedimento com quantos arquivos forem necessários.

# Dashboard
O dashboard conta com 3 páginas, cada uma com um objetivo diferente.
1. Visão geral    
2. Comparação entre leitos clínicos e leitos de UTI
3. Detalhamento de unidades de saúde

## Overview
![dashboard página 1 - visão geral](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/overview-8x.gif?raw=true)
## Leitos Clínicos e Leitos de UTI
![dashboard página 2 - comparação entre ocupação de leitos clínicos e leitos UTI](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/type-8x.gif?raw=true)
## Detalhamento de Unidades de Saúde
![dashboard página 3 - detalhamento indvidual de unidades de saúde](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/type-8x.gif?raw=true)

# Modelagem
![esquema da modelagem de dados]()

# Fonte de dados
Da mesma maneira como feito no projeto [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital) os dados foram coletados do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/registro-de-ocupacao-hospitalar-covid-19). São dados relacionados a ocupação hospitalar com foco em casos suspeitos e confirmados de COVID-19. No momento a fonte dispõe de registros dos anos 2020, 2021 e 2022. Não há menção se os dados serão atualizados.

Ainda do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/registro-de-ocupacao-hospitalar-covid-19), temos outro [endpoint](https://dados.gov.br/dados/conjuntos-dados/hospitais-e-leitos) fornecendo dados sobre unidades de saúde, contendo informações sobre nome e localidade. Informações sobre o tamanho da população de cada estado foram retiradas deste [painel](https://infoms.saude.gov.br/extensions/covid-19_html/covid-19_html.html) do Ministério da Saúde.

| Conjunto de dados | Data de coleta |
| ----------------- | -------------- |
| Leitos | 07/02/2024 |
| Ocupação | 07/02/2024 |
| População | 22/03/2024 |

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
```
# https://github.com/Textualize/rich
pip install rich
```