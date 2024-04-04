from colorama import Fore, Style, init
import random
import subprocess

# import json
# import os

# if __package__ is None or __package__ == '':
#     from dmtoolbox.osFuncs import *
# else:
#     from .osFuncs import *



# Functions
__all__ = ['check_port_availability', 'find_available_ports', 'find_port', 'setup_available_port']

# Variables
__all__ += ['PREFERRED_PORTS', 'AVAILABLE_PORT']


PREFERRED_PORTS = [
    49200,
    49300,
    49400,
    49500,
    49600,
    49700,
    49800,
    49900,
    50100,
    50200 
]

AVAILABLE_PORT = PREFERRED_PORTS[0]

DEFAULT_HOSTNAME = 'teste_de_aplicação'

init() 


def check_port_availability(port, host='127.0.0.1', hostname=DEFAULT_HOSTNAME):
    """
    Verifica a disponibilidade de uma porta em um determinado host.

    Parâmetros:
    -----------
    - port: int
        - O número da porta a ser verificado.
    - host: str (opcional, padrão='127.0.0.1')
        - O endereço IP do host onde a porta será verificada.

    Retorno:
    --------
    - bool
        - True se a porta estiver disponível, False caso contrário.

    Exemplo:
    --------
    >>> check_port_availability(80)
    False
    >>> check_port_availability(5000, 'localhost')
    True

    Nota:
    -----
    Este método verifica a disponibilidade de uma porta específica em um host. 
    Ele primeiro encontra o PID usando a porta especificada, e então verifica se o processo associado a esse PID é 'nginx' ou o hostname
    indicado.
    Esta função depende do comando 'netstat' no Windows para verificar o estado das portas.
    É importante observar que a disponibilidade da porta pode mudar instantaneamente após a verificação,
    especialmente em ambientes de rede dinâmica.
    """

    command_find_pid = f'netstat -aon | findstr /R /C:"{host}:{port}"'
    result_find_pid = subprocess.run(command_find_pid, capture_output=True, text=True, shell=True)

    if result_find_pid.stdout:
        lines = result_find_pid.stdout.strip().split('\n')
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 4 and parts[1] == f'{host}:{port}':
                pid = parts[-1]
                command_find_process = f'tasklist /FI "PID eq {pid}"'
                result_find_process = subprocess.run(command_find_process, capture_output=True, text=True, shell=True)
                
                if "nginx" in result_find_process.stdout.lower() or hostname in result_find_process.stdout.lower():
                    return True
                
        return False
    else:
        
        return True   
    
def find_available_ports(start_port, end_port, host='127.0.0.1', hostname=DEFAULT_HOSTNAME):
    """
    Encontra portas disponíveis em um dado range.

    Parâmetros:
    -----------
    - start_port: int
        - Início do intervalo de portas a ser verificado.
    - end_port: int
        - Fim do intervalo de portas a ser verificado.
    - host: str (opcional, padrão='127.0.0.1')
        - Endereço IP para verificar a disponibilidade das portas.
    - hostname: str (opcional, padrão='teste_de_aplicação')
        - Nome do host para verificar a disponibilidade das portas.

    Retorno:
    --------
    - list
        - Lista de portas disponíveis no intervalo especificado.

    Exemplo:
    --------
    >>> find_available_ports(49152, 49155)
    [49152, 49153, 49154]

    Nota:
    -----
    Esta função verifica a disponibilidade de portas em um intervalo específico.
    Retorna uma lista das portas disponíveis dentro do intervalo especificado.
    """
    available_ports = []
    for port in range(start_port, end_port + 1):
        if check_port_availability(port, host, hostname):
            available_ports.append(port)
    return available_ports

def find_port_internal(preferred_ports=PREFERRED_PORTS, hostname=DEFAULT_HOSTNAME):
    """
    Encontra uma porta disponível, tentando as portas preferidas primeiro.

    Parâmetros:
    -----------
    - preferred_ports: list (opcional, padrão=PREFERRED_PORTS)
        - Lista de portas preferidas a serem verificadas primeiro.
    - hostname: str (opcional, padrão='teste_de_aplicação')
        - Nome do host para verificar a disponibilidade das portas.

    Retorno:
    --------
    - int
        - A porta disponível encontrada.

    Levanta:
    --------
    - Exception
        - Se não for possível encontrar uma porta disponível.

    Exemplo:
    --------
    >>> find_port_internal()
    49200

    Nota:
    -----
    Esta função tenta encontrar uma porta disponível, primeiro verificando as portas preferidas,
    depois portas aleatórias no intervalo de 49152 a 65536 e finalmente todas as portas nesse intervalo, se necessário.
    """
    # Etapa 1: Verificar portas pré-definidas
    for port in preferred_ports:
        if check_port_availability(port, hostname=hostname):
            return port

    # Etapa 2: Testar 100 portas aleatórias
    try:
        random_ports = random.sample(range(49152, 65536), 100)
    except ValueError:
        # Caso a geração de portas aleatórias falhe devido ao range ser pequeno
        random_ports = range(49152, 65536)
    
    for port in random_ports:
        if check_port_availability(port, hostname=hostname):
            return port

    # Etapa 3: Testar todas as portas no intervalo, se necessário
    for port in range(49152, 65536):
        if check_port_availability(port, hostname=hostname):
            return port

    # Se nenhuma porta disponível for encontrada, lança uma exceção personalizada
    raise Exception("Não foi possível encontrar uma porta disponível. Verifique a configuração da rede.")

def find_port(hostname=DEFAULT_HOSTNAME):
    """
    Encontra uma porta disponível.

    Parâmetros:
    -----------
    - hostname: str (opcional, padrão='teste_de_aplicação')
        - Nome do host para verificar a disponibilidade das portas.

    Nota:
    -----
    Esta função tenta encontrar uma porta disponível, utilizando as portas preferidas definidas.
    Se não for possível encontrar uma porta disponível, uma mensagem de erro será exibida em vermelho.
    """
    try:
        return find_port_internal(hostname)
    except Exception as e:
        print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)

    
# def setup_available_port():
#     global METADATA
#     metadata_file = METADATA
#     metadata = {}

#     # Verifica se o arquivo METADATA já existe e lê seu conteúdo
#     if os.path.exists(metadata_file):
#         with open(metadata_file, 'r') as file:
#             try:
#                 metadata = json.load(file)
#             except json.JSONDecodeError:
#                 metadata = {}

#     # Verifica se 'AVAILABLE_PORT' está em 'metadata'
#     if 'AVAILABLE_PORT' in metadata:
#         if check_port_availability(metadata['AVAILABLE_PORT']):
#             # A porta armazenada está disponível
#             return metadata['AVAILABLE_PORT']
#         else:
#             # A porta armazenada não está disponível, encontra uma nova
#             new_port = find_port()
#     else:
#         # 'AVAILABLE_PORT' não está em 'metadata', encontra uma nova
#         new_port = find_port()

#     # Atualiza 'metadata' com a nova porta disponível e salva no arquivo
#     metadata['AVAILABLE_PORT'] = new_port
    
#     if not os.path.exists(metadata_file):
#         create_appdata()
    
#     with open(metadata_file, 'w') as file:
#         json.dump(metadata, file, indent=4)
    
#     return new_port

# TODO Ajeitar a função para dar imput na porta para o nginx e para o servidor flask

def setup_available_port(hostname=DEFAULT_HOSTNAME):
    """
    Configura uma porta disponível.

    Parâmetros:
    -----------
    - hostname: str (opcional, padrão='teste_de_aplicação')
        - Nome do host para verificar a disponibilidade das portas.

    Retorno:
    --------
    - int
        - A porta disponível configurada.

    Nota:
    -----
    Esta função configura uma porta disponível, utilizando as portas preferidas definidas.
    """
    return find_port_internal(PREFERRED_PORTS, hostname)


if __name__ == '__main__':
    pass



