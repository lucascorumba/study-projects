import utils
import cleaner
import sys
import warnings
from rich.console import Console


def update_lookup():
    """
    Função chamada para limpeza e junção de registros referentes à identificadores de unidades de saúde.
    Lê nomes de arquivos fornecidos como argumentos na linha de comando.
    Executa processos de redução e limpeza, Mantém apenas:
        * Identificador, nome fantasia, município, UF e região.
    Reúne os diversos arquivos fornecidos, remove redundâncias e salva um novo .csv completo.
    """
    # Captura nome dos arquivos em uma lista de strings
    console = Console()
    args, out_files = sys.argv[2:], list()
    console.print('[i]\nTratando dimensões...\n[/i]')
    with console.status('[bold green]Trabalhando nas tarefas...[/bold green]') as status:
        for arg in args:
            # Abre arquivo            
            df = pd.read_csv(f'{arg}')
            # Seleciona colunas de interesse
            df = df[['CNES', 'NOME ESTABELECIMENTO', 'MUNICIPIO', 'UF']]
            # Remove redundâncias
            df = df.drop_duplicates(subset=['CNES'])
            # Cria nome para arquivo processado
            file_name = f'{arg.split(".")[0]}-clean.csv'
            # Salva novo .csv
            df.to_csv(f'{file_name}', index=False, encoding='utf-8')
            # Adiciona nome do arquivo em lista para concatenação
            out_files.append(file_name)
            console.print(f'\t{arg} ---- [green]OK[/green]')
        console.print('\nArquivos limpos com sucesso', style='green')
        # Concatena arquivos gerados
        utils.concat_df(out_files, True)
        console.print('\nArquivos concatenados com sucesso', style='green')


def update_fact(lookup):
    """
    Função chamada para processamento e junção de dados referentes à ocupação de unidades de saúde.
    Lê nomes de arquivos fornecidos como argumentos na linha de comando.
    Executa processos de redução e limpeza.
    Reúne os diversos arquivos fornecidos e salva um novo .csv completo.
    """
    # Captura nome dos arquivos em uma lista de strings
    console = Console()
    args, out_files = sys.argv[2:], list()
    console.print('[i]\nTratando dados...\n[/i]')
    with console.status('[bold green]Trabalhando nas tarefas...[/bold green]') as status:
        for arg in args:
            # Gera nome para arquivo processado
            file_name = f'{arg.split(".")[0]}-clean.csv'
            # Adiciona nome do arquivo em lista para concatenação
            out_files.append(file_name)
            # Realiza limpeza e processamento
            df = cleaner.clean_fact(arg, lookup)        
            # Salva novo .csv
            df.to_csv(f'{file_name}', index=False, encoding='utf-8')        
            console.print(f'\t{arg} ---- [green]OK[/green]')
        console.print('\nProcessamento concluído com sucesso', style='green')
        # Concatena arquivos processados
        utils.concat_df(out_files)
        console.print('\nArquivos concatenados com sucesso', style='green')


if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=DeprecationWarning)
    import pandas as pd

    args, out_files = sys.argv[2:], list()
    if sys.argv[1] == "lookup":
        update_lookup()
    elif sys.argv[1] == "fact":
        update_fact('leitos-concat.csv')
    else:
        print("Função não encontrada. Selecione:\n\t* 'lookup' para processar a tabela dimensão\n\
        * 'fact' para processar a tabela fato\nUso: >>>python main.py lookup file_0.csv ... file_n.csv")