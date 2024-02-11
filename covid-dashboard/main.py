import utils
import cleaner
import sys
import warnings
#from rich.console import console


def update_lookup():
    """
    Função chamada para limpeza e junção de registros referentes à registro de unidades de saúde.
    Lê nomes de arquivos fornecidos como argumentos na linha de comando.
    Executa processos de redução e limpeza, Mantém apenas:
        * Identificador, nome fantasia, município, UF e região.
    Reúne os diversos arquivos fornecidos, remove redundâncias e salva um novo .csv completo.
    """
    print('Tratando dimensões')
    # Captura nome dos arquivos em uma lista de strings
    args, out_files = sys.argv[2:], list()
    for arg in args:
        # Abre arquivo
        df = pd.read_csv(f'{arg}')
        # Seleciona colunas de interesse
        df = df[['CNES', 'NOME ESTABELECIMENTO', 'MUNICIPIO', 'UF', 'REGIAO']]
        # Remove redundâncias
        df = df.drop_duplicates(subset=['CNES'])
        # Cria nome para arquivo processado
        file_name = f'{arg.split(".")[0]}-clean.csv'
        # Salva novo .csv
        df.to_csv(f'{file_name}', index=False, encoding='utf-8')
        # Adiciona nome do arquivo em lista para concatenação
        out_files.append(file_name)
        print(f'\t{file_name} ---------- OK')
    # Concatena arquivos gerados
    utils.concat_df(out_files, True)


def update_fact(lookup):
    """
    lorem ipsum lookup -> .csv filename of lookup table
    """
    # Captura nome dos arquivos em uma lista de strings
    args, out_files = sys.argv[2:], list()
    for arg in args:
        # Gera nome para arquivo processado
        file_name = f'{arg.split(".")[0]}-clean.csv'
        # # Adiciona nome do arquivo em lista para concatenação
        out_files.append(file_name)
        # Realiza limpeza e processamento
        df = cleaner.clean_fact(arg, lookup)        
        # Salva novo .csv
        df.to_csv(f'{file_name}', index=False, encoding='utf-8')        
        print(f'\t{file_name} ---------- OK')
    # Concatena arquivos ferados
    utils.concat_df(out_files)


if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=DeprecationWarning)
    import pandas as pd

    args, out_files = sys.argv[2:], list()
    if sys.argv[1] == "lookup":
        update_lookup()
    elif sys.argv[1] == "fact":
        print('Iniciando processo')
        update_fact('leitos-concat.csv')
    else:
        print("Função não encontrada. Selecione:\n\t* 'lookup' para processar a tabela dimensão\n\
        * 'fact' para processar a tabela fato\nUso: >>>python main.py lookup file_0.csv ... file_n.csv")