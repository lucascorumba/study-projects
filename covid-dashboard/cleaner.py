import pandas as pd
import numpy as np
from datetime import date
import warnings
import utils


def clean_fact(fact, lookup):
    """
    Recebe dois nomes de arquivos .csv, um direcionando aos registros que formarão a tabela fato e outro para dimensão.
    Realiza o processamento dos dados em 'fact' e salva os dados preparados em um arquivo .csv.
    """
    # Suprime avisos no console sobre implementações futuras
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Carrega tabela fato ocupação
    df = pd.read_csv(f'{fact}', low_memory=False)
    # Extrai apenas ano do nome do arquivo
    cur_year = int(fact.split(".")[0].split('-')[1])

    ## Remover registros da tabela fato não mapeados 
    # Corrige registros com erros de preenchimento no identificador
    df['cnes'] = pd.to_numeric(df['cnes'], errors='coerce', downcast='unsigned')
    # Erros que não puderam ser corrigidos (marcados como NaN) são removidos
    df.dropna(subset=['cnes'], inplace=True)
    # Corrige tipo de dado da coluna 'cnes': float -> uint32
    df['cnes'] = df['cnes'].astype(np.uint32)

    # Carregar tabela dimensão leitos
    df_lookup = pd.read_csv(f'{lookup}')
    # Remove de 'fact' registros não mapeados em 'lookup'
    df = df[df['cnes'].isin(df_lookup['CNES'])] 

    ## Etapas de limpeza
    df.drop(df.loc[df['excluido'] == True].index, inplace=True)
    df.drop(df.loc[df['estado'].isnull()].index, inplace=True)
    df.drop(df.loc[df['estado'] != df['estadoNotificacao']].index, inplace=True)
    df.drop(df.loc[df['municipio'] != df['municipioNotificacao']].index, inplace=True)

    # Para comportar as alterações feitas de em arquivos a partir de 2022
    if cur_year >= 2022:
        df['ocupacaoConfirmadoCli'] = df['ocupacaoHospitalarCli']
        df['ocupacaoConfirmadoUti'] = df['ocupacaoHospitalarUti']
        # Mapeia registros onde 'OcupacaoHospitalar...' é ausente
        mark_cli = df['ocupacaoHospitalarCli'].isna()
        mark_uti = df['ocupacaoHospitalarUti'].isna()
        # Mantém como NaN registros que orginalmente possuiam NaN
        df.loc[~mark_cli, 'ocupacaoSuspeitoCli'] = 0
        df.loc[~mark_uti, 'ocupacaoSuspeitoUti'] = 0

    # Remoção de campos não usados
    to_drop_numeric = ['Unnamed: 0', 'ocupacaoCovidUti', 'ocupacaoCovidCli', 'ocupacaoHospitalarUti', 'ocupacaoHospitalarCli']
    df.drop(columns=to_drop_numeric, inplace=True)

    # Adiciona coluna 'uf' com base no nome do estado
    #df['uf'] = df['estado'].apply(lambda x: utils.get_uf(x, utils.uf_dict))

    ## Substituíndo outliers por NaN
    # Leitos Clínicos
    drop_indexes = df.loc[(df['ocupacaoSuspeitoCli'] + df['ocupacaoConfirmadoCli']) > 1843].index
    target_cols = ['ocupacaoSuspeitoCli', 'ocupacaoConfirmadoCli']
    for item in drop_indexes:
        for col in target_cols:
            df.loc[item, col] = np.NaN
    # Leitos UTI
    drop_indexes = df.loc[(df['ocupacaoSuspeitoUti'] + df['ocupacaoConfirmadoUti']) > 380].index
    target_cols = ['ocupacaoSuspeitoUti', 'ocupacaoConfirmadoUti']
    for item in drop_indexes:
        for col in target_cols:
            df.loc[item, col] = np.NaN
    # Altas
    drop_indexes = df.loc[(df['saidaSuspeitaObitos'] + df['saidaSuspeitaAltas'] + df['saidaConfirmadaObitos']\
                            + df['saidaConfirmadaAltas']) > 1843 + 380].index
    target_cols = ['saidaSuspeitaObitos', 'saidaSuspeitaAltas', 'saidaConfirmadaObitos', 'saidaConfirmadaAltas']
    for item in drop_indexes:
        for col in target_cols:
            df.loc[item, col] = np.NaN

    ## Substituindo valores negativos por NaN
    cols = ['ocupacaoSuspeitoCli', 'ocupacaoSuspeitoUti', 'ocupacaoConfirmadoCli', 'ocupacaoConfirmadoUti', \
            'saidaSuspeitaObitos', 'saidaSuspeitaAltas', 'saidaConfirmadaObitos', 'saidaConfirmadaAltas']

    for col in cols:
        df[col] = df[col].apply(lambda x: utils.check_negative(x))

    ## Substituíndo valores contínuos por NaN
    for col in cols:
        df[col] = df[col].apply(lambda x: utils.check_int(x))

    ## Imputando dados - mediana
    for col in cols:
        df[col].fillna(df[col].median(), inplace=True)

    ## Otimizando o armazenamento
    # Transforma a coluna 'dataNotificacao' do tipo 'object' para o tipo 'datetime64'
    df['dataNotificacao'] = pd.to_datetime(df['dataNotificacao'])
    # Cria coluna 'data' no formato YYYY-MM-DD com base em 'dataNotificacao'
    df['data'] = df['dataNotificacao'].dt.date

    # transforma colunas numéricas 'float64' em 'uint16'
    for col in cols:
        df[col] = pd.to_numeric(df[col], downcast='unsigned')

    # Removendo colunas não usadas
    to_drop = ['dataNotificacao', 'municipioNotificacao', 'estado', 'estadoNotificacao', 'validado', 'origem', \
                '_id', '_p_usuario', '_created_at', '_updated_at', 'excluido']
    df.drop(columns=to_drop, inplace=True)

    ## Adicionando colunas calculadas
    df['totalOcupacaoCli'] = df['ocupacaoSuspeitoCli'] + df['ocupacaoConfirmadoCli']
    df['totalOcupacaoUti'] = df['ocupacaoSuspeitoUti'] + df['ocupacaoConfirmadoUti']
    df['totalOcupacao'] = df['totalOcupacaoCli'] + df['totalOcupacaoUti']
    df['totalAltas'] = df['saidaSuspeitaAltas'] + df['saidaConfirmadaAltas']
    df['totalObitos'] = df['saidaSuspeitaObitos'] + df['saidaConfirmadaAltas']
    df['totalSaidas'] = df['totalAltas'] + df['totalObitos']
    #df['regiao'] = df['uf'].apply(lambda x: utils.get_region(x, utils.region_dict))

    to_drop = ['ocupacaoSuspeitoCli', 'ocupacaoConfirmadoCli', 'ocupacaoSuspeitoUti', 'ocupacaoConfirmadoUti']
    df.drop(columns=to_drop, inplace=True)
    
    ## Erro de preenchimento - seção "Correções Necessárias" do trabalho "covid-hospital"

    # listas temporárias para valores de saída / 
    jan_ago, set_dez = list(), list()
    # lista com ids de 'cnes' marcadas para exclusão - substituída pelo conjunto utils.faulty_cnes
    # drop_cnes = list() 
    # limite para separar datas em jan/ago e set/dez
    sep_date = date(cur_year, 9, 1)

    # suprime RankWarning - este aviso é sinalizado quando há poucos pontos para uma linha mais precisa
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        # itera por todas as cnes registradas
        for cnes in df['cnes'].unique():
            temp = df.loc[df['cnes'] == cnes].copy()
            # ordena registros por data -> mais recentes antes
            temp.sort_values(by='data', ascending=True, inplace=True)
            
            # separa registros em jan/ago e set/dez
            for i in range(len(temp)):
                if temp['data'].iloc[i] < sep_date:
                    jan_ago.append(temp['totalSaidas'].iloc[i])
                else:
                    set_dez.append(temp['totalSaidas'].iloc[i])
            # ajusta parâmetros para polyfit()
            x1 = np.arange(len(jan_ago))
            x2 = np.arange(len(set_dez))

            try:
                # inicializa variáveis para evitar NameError após possível TypeError
                coef_a1, coef_l1, coef_a2, coef_l2 = int(), int(), int(), int()
                # gera polinômios e seleciona coeficientes angulares
                coef_l1, coef_a1 = np.polynomial.polynomial.polyfit(x1, jan_ago, 1)
                coef_l2, coef_a2 = np.polynomial.polynomial.polyfit(x2, set_dez, 1)
            # TypeError é sinalizado quando um vetor vazio é fornecido como parâmetro para polyfit
            except TypeError:
                # apenas registros vazios
                if (not coef_a1) and (not coef_a2):
                    utils.clear_lists(jan_ago, set_dez)
                    continue
                # onde só há um conjunto, testa apenas o coeficiente angular presente
                if ((coef_a1) and (coef_a1 < 5)) or ((coef_a2) and (coef_a2 < 5)):
                    utils.clear_lists(jan_ago, set_dez)
                    continue
                # coeficiente angular maior que 5 -> marca para exclusão
                else: 
                    utils.faulty_cnes.add(cnes)
                    utils.clear_lists(jan_ago, set_dez)
                    continue

            # valor absoluto máximo aceitável para coeficientes -> linear: 50 | angular: 5
            if (abs(coef_a1) >= 5) or (abs(coef_a2) >= 5) or (abs(coef_l1) >= 50) or (abs(coef_l2) >= 50):
                utils.faulty_cnes.add(cnes)
                utils.clear_lists(jan_ago, set_dez)
                continue

            # aplica teste entre coeficientes angulares jan/ago e set/dez -> tolerância de 3.5x (250%)
            a, b = utils.big_small(coef_a1, coef_a2)
            if np.allclose(a, b, rtol=2.5):
                utils.clear_lists(jan_ago, set_dez)
                continue
            else:
                # tolerância absoluta de 1 entre conjuntos recusados pelo teste anterior        
                if np.allclose(a, b, atol=1):
                    utils.clear_lists(jan_ago, set_dez)
                    continue      
                utils.faulty_cnes.add(cnes)
            # limpa listas para próximo loop
            utils.clear_lists(jan_ago, set_dez)
    df.drop(df.loc[df['cnes'].isin(utils.faulty_cnes)].index, inplace=True)
    return df