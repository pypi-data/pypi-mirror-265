import os
import ctypes
import platform
import sys
import shutil
import subprocess



# Functions
__all__ = ['get_script_directory',
           'is_admin', 
            'raise_admin', 
            'is_installed',
            'write_file',
            'copy_file',
            'verify_dependencies',
            'in_virtualenv',
            'try_import_or_install',
            'run_command'
        ]

# Variables
__all__ += ['DIR_PATH', 'PKG_DEPENDENCIES']

PKG_DEPENDENCIES = ['pandas', 'openpyxl', 'jinja2', 'numpy', 'prettytable', 'colorama', 'pyinstaller']


def get_script_directory():
    """
    Retorna o diretório do script atual, funcionando tanto para scripts Python
    executados diretamente quanto para executáveis gerados pelo PyInstaller.

    Retorno:
    --------
    - str
        - O caminho completo do diretório do script atual.
    """
    if getattr(sys, 'frozen', False):
        # Caminho do executável quando o script é empacotado pelo PyInstaller.
        script_directory = os.path.dirname(sys.executable)
    else:
        # Caminho normal quando o script é executado como um script Python.
        script_directory = os.path.dirname(os.path.abspath(__file__))
    return script_directory

DIR_PATH = get_script_directory()


def in_virtualenv():
    """
    Verifica se o script está sendo executado dentro de um ambiente virtual.

    Retorno:
    --------
    - bool
        - True se estiver em um ambiente virtual, False caso contrário.
    """
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def try_import_or_install(package_name, module_name=None):
    """
    Tenta importar um módulo Python e, se falhar, oferece ao usuário a opção de instalá-lo.

    Parâmetros:
    -----------
    - package_name: str
        - O nome do pacote Python a ser importado ou instalado.
    - module_name: str (opcional)
        - O nome do módulo dentro do pacote (se diferente do nome do pacote).

    Nota:
    -----
    Esta função tenta importar o módulo especificado. Se o módulo não puder ser importado,
    o usuário será solicitado a instalar o pacote correspondente. Esta função usa 'pip' para instalar pacotes.
    """
    if module_name is None:
        module_name = package_name
    try:
        __import__(module_name)
    except ImportError:
        user_decision = input(f'O módulo {module_name} é necessário mas não foi encontrado. Deseja instalar {package_name}? (y/n): ')
        if user_decision.lower() == 'y':
            if not in_virtualenv() and platform.system() == 'Windows' and not is_admin():
                raise_admin()
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            
def is_admin():
    """
    Verifica se o script está sendo executado com privilégios de administrador.

    Retorno:
    --------
    - bool
        - True se estiver sendo executado com privilégios de administrador, False caso contrário.
    """
    os_name = platform.system()
    
    if os_name == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:  # Isso cobrirá Linux, Darwin (macOS) e outras variantes Unix
        try:
            return os.getuid() == 0
        except AttributeError:
            return False
       
def raise_admin():
    """
    Eleva os privilégios do script para administrador.

    Nota:
    -----
    Esta função solicitará privilégios de administrador no Windows e instruirá o usuário
    a reiniciar o script com privilégios elevados em sistemas não Windows.
    """
    if not is_admin():
        os_name = platform.system()
        if os_name == 'Windows':
            # Solicita elevação de privilégios e reinicia o script no Windows
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(f'"{arg}"' for arg in sys.argv), None, 1)
            sys.exit(0)
        else:
            # Para sistemas não Windows, instrui o usuário a reiniciar o script com privilégios elevados
            print("Este script precisa ser executado com privilégios de administrador. Por favor, reinicie o script usando 'sudo' (Linux/macOS).")
            sys.exit(1)      

def is_installed(destination, filename):
    """
    Verifica se um arquivo está instalado em um diretório específico.

    Parâmetros:
    -----------
    - destination: str
        - O diretório onde o arquivo deve ser verificado.
    - filename: str
        - O nome do arquivo a ser verificado.

    Retorno:
    --------
    - bool
        - True se o arquivo estiver instalado, False caso contrário.
    """

    # Checks if the file exists in the destination directory
    full_path = os.path.join(destination, filename)
    return os.path.exists(full_path)

def write_file(new_file_content, file_path, overwrite=True):
    """
    Escreve ou anexa conteúdo em um arquivo.

    Parâmetros:
    -----------
    - new_file_content: str
        - O conteúdo a ser escrito no arquivo.
    - file_path: str
        - O caminho completo do arquivo.
    - overwrite: bool (opcional, padrão=True)
        - Se True, substitui o conteúdo existente no arquivo. Se False, anexa ao conteúdo existente.

    Nota:
    -----
    Esta função escreve ou anexa o conteúdo fornecido no arquivo especificado.
    """
   
    if overwrite:    
        with open(file_path, 'w', encoding='utf-8') as file:  # Adiciona 'encoding="utf-8"'
            file.write(new_file_content)
    else: 
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            
        file_content += new_file_content
        
        with open(file_path, 'w', encoding='utf-8') as file:  # Adiciona 'encoding="utf-8"'
            file.write(file_content)

def copy_file(origin, destination, new_filename=None):
    """
    Copia um arquivo de 'origin' para 'destination', permitindo a mudança do nome do arquivo de destino.

    Parâmetros:
    -----------
    - origin: str
        - O caminho completo do arquivo de origem.
    - destination: str
        - O diretório de destino para o arquivo.
    - new_filename: str (opcional)
        - Novo nome para o arquivo no destino.

    Nota:
    -----
    Esta função copia o arquivo especificado de 'origin' para 'destination',
    permitindo a mudança do nome do arquivo no destino.
    """
    """
    Copia um arquivo de 'origin' para 'destination', permitindo a mudança do nome do arquivo de destino.

    :param origin: O caminho completo do arquivo de origem.
    :param destination: O diretório de destino para o arquivo.
    :param new_filename: Novo nome para o arquivo no destino (opcional).
    """
    try:
        # Certifica-se de que o diretório de destino existe, cria se necessário
        os.makedirs(destination, exist_ok=True)

        # Define o caminho completo do destino incluindo o novo nome do arquivo, se fornecido
        if new_filename:
            destination_path = os.path.join(destination, new_filename)
        else:
            destination_path = os.path.join(destination, os.path.basename(origin))
        
        # Copia o arquivo
        shutil.copyfile(origin, destination_path)
        print(f"Arquivo copiado para '{destination_path}' com sucesso.")
    except FileNotFoundError:
        print(f"Erro: O arquivo de origem '{origin}' não foi encontrado.")
    except PermissionError:
        print("Erro de permissão: Não foi possível copiar o arquivo. Verifique as permissões.")
    except Exception as e:
        print(f"Erro ao copiar o arquivo: {e}")

def verify_dependencies(dependencies=[], to_verify=''):
    """
    Verifica se os módulos Python necessários estão instalados.

    Parâmetros:
    -----------
    - dependencies: list (opcional)
        - Lista de módulos Python a serem verificados.
    - to_verify: str (opcional)
        - Indica se os módulos a serem verificados são dependências de pacotes (PKG_DEPENDENCIES)
          ou módulos gerais (dependencies).

    Retorno:
    --------
    - bool
        - True se todos os módulos estiverem instalados, False caso contrário.
    """
    
    if to_verify == '':
        required_modules = dependencies
    elif to_verify == 'pkg':
        required_modules = PKG_DEPENDENCIES
    else:
        print('Comando não reconhecido, verifique o arguemento "to_verify"')
        return None
    
    
    
    for mod in required_modules:
        try:
            __import__(mod)
        except ModuleNotFoundError:
            print(f'\nErro: O módulo "{mod}" é necessário mas não foi encontrado.')
            print(f'Por favor, instale o "{mod}" executando: pip install {mod}\n')
            return False
    return True

def run_command(command):
    """
    Executa um comando no shell e imprime a saída ou o erro.

    Parâmetros:
    -----------
    - command: str
        - O comando a ser executado.

    Nota:
    -----
    Esta função executa o comando especificado no shell e imprime a saída ou o erro resultante.
    """
    try:
        # Executa o comando e captura a saída (stdout) e o erro (stderr)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        # Verifica se o comando foi executado com sucesso (código de saída 0)
        if result.returncode == 0:
            print("Saída do comando:")
            print(result.stdout)
        else:
            print("Erro ao executar o comando:")
            print(result.stderr)
    except Exception as e:
        print(f"Ocorreu um erro ao executar o comando: {e}")

if __name__ == '__main__':
    pass
