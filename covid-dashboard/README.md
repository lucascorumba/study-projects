# Ocupação Hospitalar - Dashboard
Este projeto busca melhorar o anterior [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital), onde foi feito um tratamento completo de dados brutos obtidos sobre ocupação hospitalar. Nisso se inclui detecção de anomalias e erros no preenchimento, imputação de dados faltantes e criação de colunas calculadas. Aqui ainda foi utilizado outro conjunto de dados referente ao detalhamento de unidades de saúde. Unificando ambas fontes de dados através de relacionamento por chaves é possível detalhar ainda mais as informações do trabalho anterior.

Outra melhora importante é a unificação de registros de diversos anos. Enquanto o anterior se limitava ao ano de 2020, esse projeto automatizou a unificação de dados. No momento apenas os anos 2020, 2021 e 2022 estão disponíveis na fonte, mas os scripts estão preparados para receber quantos arquivos forem fornecidos futuramente. Mais detalhes sobre a obtenção dos dados em [Fonte de dados](#3)

A etapa de visualização foi substituida pela criação de um [Dashboard](#2) no Power BI.

# Sumário
* [Processamento](#1)
* [Dashboard](#2)
    * [Overview](#2-a)
    * [Leitos Clínicos e Leitos de UTI](#2-b)
    * [Detalhamento de Unidades de Saúde](#2-c)
* [Fonte de dados](#3)
* [Cronograma](#4)
* [Requisitos](#5)

# Processamento<a id="1"></a>
Com os dados brutos obtidos, os scripts realizam o processamento, limpeza e unificação dos dados.
Primeiro preparamos o arquivo que será base para a tabela dimensão de leitos:
![execução do processo de limpeza e unificação da tabela dimensão](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/record-lookup.gif?raw=true)

Em seguida fazemos o mesmo com a os arquivos base para a tabela fato de ocupação hospitalar:
![execução do processo de limpeza e unificação da tabela fato](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/record-fact.gif?raw=true)

Ao executar arquivo `main.py` podemos escolher qual operação realizar. Passando o parâmetro `lookup` realizamos o processamento de arquivos relaciocados à leitos. Com o parâmetro `fact` fazemos o processo adaptado do projeto [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital).
Em ambas situações os próximos parâmetros na linha de comando são arquivos `.csv`. Aqui usamos dos anos 2020, 2021 e 2022 já que são os disponíveis. Mas, caso haja atualização, os scripts realizam o mesmo procedimento com quantos arquivos forem necessários.

# Dashboard<a id="2"></a>
O dashboard conta com 3 páginas, cada uma com um objetivo diferente.
1. Visão geral    
2. Comparação entre leitos clínicos e leitos de UTI
3. Detalhamento de unidades de saúde

## Overview<a id="2-a"></a>
![dashboard página 1 - visão geral](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/overview-8x.gif?raw=true)

Aqui se encontram **informações gerais** e diversas KPIs. Todas as informações a seguir podem ser filtradas por **data** e **localidade** simultaneamente:
* Tamanho da população
* Ocupação acumulada
* Média de ocupação hospitalar
* Óbitos acumulados
* Taxa de óbitos por 100 mil habitantes
* Número de unidades de saúde mapeadas
* Número de municípios mapeados
* Relação entre número de altas e número de óbitos
* % do total de óbitos em cada localidade
* Estados ordenados por ocupação acumulada

## Leitos Clínicos e Leitos de UTI<a id="2-b"></a>
![dashboard página 2 - comparação entre ocupação de leitos clínicos e leitos UTI](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/type-7x.gif?raw=true)

Essa página é dedicada a comparação entre **leitos clínicos e leitos de UTI**. Todas as informações podem ser filtradas por **data** e **localidade** simultaneamente:
* Ocupação acumulada por região
* Ocupação acumulada de leitos clínicos e leitos UTI
* Média de ocupação de leitos clínicos e leitos UTI
* Correlação entre ocupação de leitos clínicos e leitos UTI
* Proporção entre ocupação de leitos clínicos e leitos UTI
* Ocupação de leitos clínicos
* Ocupação de leitos UTI

## Detalhamento de Unidades de Saúde<a id="2-c"></a>
![dashboard página 3 - detalhamento indvidual de unidades de saúde](https://github.com/lucascorumba/study-projects/blob/main/readme-imgs/covid-dashboard/single-8x.gif?raw=true)

Aqui se encontram detalhes de **unidades de saúde**. As unidades com maior ocupação acumulada são dispostas em ordem na lista. Todas as informações podem ser filtradas por **data** e **localidade** simultaneamente:
* Nome, localidade e código da unidade de saúde em questão
* Ocupação total
* Ocupação de leitos clínicos
* Ocupação de leitos UTI
* Ocupação por trimestre
* Média de ocupação por trimestre
* Ocupação total por trimestre
* Comparação da ocupação com o trimestre anterior
* Comparação da média com o trimestre anterior
* Relação entre número de altas e número de óbitos por unidade de saúde
* Total de óbitos por unidade de saúde
* Média de ocupação por unidade de saúde

# Fonte de dados<a id="3"></a>
Da mesma maneira como feito no projeto [covid-hospital](https://github.com/lucascorumba/study-projects/tree/main/covid-hospital) os dados foram coletados do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/registro-de-ocupacao-hospitalar-covid-19). São dados relacionados a ocupação hospitalar com foco em casos suspeitos e confirmados de COVID-19. No momento a fonte dispõe de registros dos anos 2020, 2021 e 2022. Não há menção se os dados serão atualizados.

Ainda do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/registro-de-ocupacao-hospitalar-covid-19), temos outro [endpoint](https://dados.gov.br/dados/conjuntos-dados/hospitais-e-leitos) fornecendo dados sobre unidades de saúde, contendo informações sobre nome e localidade. Informações sobre o tamanho da população de cada estado foram retiradas deste [painel](https://infoms.saude.gov.br/extensions/covid-19_html/covid-19_html.html) do Ministério da Saúde.

| Conjunto de dados | Data de coleta |
| ----------------- | -------------- |
| Leitos | 07/02/2024 |
| Ocupação | 07/02/2024 |
| População | 22/03/2024 |

# Cronograma<a id="4"></a>
- [x] Obtenção dos registros referentes aos seguintes anos:
    * 2020, 2021 e 2022
- [x] Obtenção dos dados referentes às unidades de atendimento
    * Criação de tabela dimensão "cnes"
- [x] Remoção de registros feitos por unidades de atendimento não mapeadas na tebela dimensão
- [x] Processamento de dados sobre ocupação - limpeza e remoção de anomalias
    * Método aplicado no projeto "covid-hospital"
    * Atenção na implementação - o arquivo agora possui diversos anos
    * Unificação dos dados para criação da tabela fato "ocupação"
- [x] Conexão com Power BI
- [x] Implementação de scripts para automatização da limpeza e unificação de registros na base de dados
- [x] Modelagem de dados
- [x] Criação de medidas com DAX
- [x] Construção dos visuais no dashboard
- [x] Gravação da demonstração do processamento de dados
- [x] Gravação da demonstração do dashboard finalizado
- [ ] Finalização do README.md

# Requisitos<a id="5"></a>
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