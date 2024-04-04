import os
from datetime import datetime
from collections import OrderedDict


__all__ = ['get_folder_size', 
           'find_default_paths', 
           'find_script_dir', 
           'find_style_sheet_path', 
           'get_file_size', 
           'get_modification_date',
           'format_size',
           'format_date',
           ]


def get_folder_size(folder_path):
    """
    Retorna o tamanho total de uma pasta em bytes.

    Parâmetros:
    -----------
    - folder_path: str
        - O caminho da pasta cujo tamanho será calculado.

    Retorno:
    --------
    - int
        - O tamanho total da pasta em bytes.
    """

    total_size = 0
    
    # Itera sobre todos os arquivos e subpastas na pasta
    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Calcula o tamanho de todos os arquivos na pasta atual
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    
    return total_size

def find_default_paths():
    """
    Encontra os caminhos padrão de pastas comuns, como Área de Trabalho, Downloads, Documentos, etc.

    Retorno:
    --------
    - dict
        - Um dicionário contendo os nomes das pastas e seus caminhos correspondentes.
    """
    # Caminhos padrão para tentar
    default_paths = OrderedDict([
        ('Área de Trabalho', ['Desktop', 'Área de Trabalho']),
        ('Downloads', 'Downloads'),
        ('Documentos', 'Documents'),
        ('Imagens', 'Pictures'),
        ('Músicas', 'Music'),
        ('Vídeos', 'Videos'),
    ])

    # Caminho base para o OneDrive no Windows
    onedrive_path = os.path.join(os.path.expanduser('~'), 'OneDrive')

    # Dicionário para armazenar os caminhos encontrados
    found_paths = {}

    for name, relative_paths in default_paths.items():
        if isinstance(relative_paths, str):
            relative_paths = [relative_paths]  # Converte em lista para unificação do tratamento
        
        for relative_path in relative_paths:
            # Verifica primeiro dentro da pasta do OneDrive
            path = os.path.join(onedrive_path, relative_path)
            if os.path.exists(path):
                found_paths[name] = path
                break
            else:
                # Se não existir no OneDrive, verifica o caminho padrão na pasta do usuário
                path = os.path.join(os.path.expanduser('~'), relative_path)
                if os.path.exists(path):
                    found_paths[name] = path
                    break
                
    found_paths['Este Computador'] = 'This PC'  # Tratado de forma especial na interface do usuário
    return found_paths

def find_script_dir():
    """
    Encontra o diretório do script atual.

    Nota:
    -----
    Esta função define uma variável global `GLOBAL_SCRIPT_DIR` que armazena o diretório do script atual.
    """
    global GLOBAL_SCRIPT_DIR
    
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if os.path.exists(script_dir):
        GLOBAL_SCRIPT_DIR = script_dir
    else:
        print(f"Erro: Diretório '{script_dir}' não encontrado")

def find_style_sheet_path(file_name):
    """
    Encontra o caminho para o arquivo de folha de estilo.

    Parâmetros:
    -----------
    - file_name: str
        - O nome do arquivo de folha de estilo.

    Nota:
    -----
    Esta função define uma variável global `GLOBAL_STYLE_PATH` que armazena o caminho para o arquivo de folha de estilo.
    """
    global GLOBAL_STYLE_PATH
    global GLOBAL_SCRIPT_DIR

    style_path = os.path.join(GLOBAL_SCRIPT_DIR, file_name)

    if os.path.exists(style_path):
        GLOBAL_STYLE_PATH = style_path
    else:
        print(f"Erro: Arquivo '{file_name}' não encontrado no diretório '{GLOBAL_SCRIPT_DIR}'.")

def get_file_size(file_path):
    """
    Retorna o tamanho de um arquivo em bytes.

    Parâmetros:
    -----------
    - file_path: str
        - O caminho do arquivo.

    Retorno:
    --------
    - int
        - O tamanho do arquivo em bytes.
    """
    return os.path.getsize(file_path)

def get_modification_date(file_path):
    """
    Retorna a data de modificação de um arquivo ou pasta.

    Parâmetros:
    -----------
    - file_path: str
        - O caminho do arquivo ou pasta.

    Retorno:
    --------
    - str
        - A data de modificação no formato ISO.
    """
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).isoformat()

def format_size(size):
    """
    Formata um tamanho em bytes para uma string legível.

    Parâmetros:
    -----------
    - size: int
        - O tamanho em bytes.

    Retorno:
    --------
    - str
        - O tamanho formatado como uma string legível.
    """

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def format_date(timestamp):
    """
    Formata um tamanho em bytes para uma string legível.

    Parâmetros:
    -----------
    - size: int
        - O tamanho em bytes.

    Retorno:
    --------
    - str
        - O tamanho formatado como uma string legível.
    """

    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass