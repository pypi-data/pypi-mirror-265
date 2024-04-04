#  ===============================================================================
#
#  Autor: Daniel Mello
#  Data: 28/02/2024
#  
#  Objetivo do módulo:
#  Este módulo contém uma coleção de funções e utilitários matemáticos e de manipulação de dados em Python.
#  Ele oferece funcionalidades como operações matriciais, formatação de dados, exportação para Excel e plotagem de gráficos.
#  O módulo foi projetado para ser reutilizável e modular, facilitando sua integração em diversos projetos.
#
#  
#  Nome: dmtoolbox
#  Este módulo foi projetado para ser importado como um módulo chamado "dmtoolbox", que contém diversas funções 
#  úteis para operações matemáticas e manipulação de dados.
#
#
#  Obs:
#  - Certifique-se de que as dependências listadas no início do módulo estão instaladas para garantir o funcionamento correto.
#  - Algumas funções podem exigir determinadas versões ou configurações específicas das bibliotecas de terceiros importadas.
#
#
#  ===============================================================================



import pandas as pd
import numpy as np
from prettytable import PrettyTable
from datetime import datetime
import matplotlib.pyplot as plt
import inspect

if __package__ is None or __package__ == '':
    from dmtoolbox.osFuncs import verify_dependencies
else:
    from .osFuncs import verify_dependencies

# Functions
__all__ = [
    'printMatrizNN',
    'printVetor',
    'separador',
    'insereMudancaLinha',
    'mat_transpose',
    'mult_matrizes',
    'round_nf',
    'count_d_places',
    'createFile',
    'export_to_excel',
    'plot_2d_function_and_compare',
    'plot_3d_function_and_arrows',
    'plot_and_compare',
    'plot_2d_function_tlwa'
]


# Variables
__all__ += ['NUMERIC_DEPENDENCIES']


NUMERIC_DEPENDENCIES = ['pandas', 'openpyxl', 'jinja2']


# ========== #
#  Formatar  #
# ========== #


def printMatrizNN (mat, headers='', transpose=True):
    """
    Imprime uma matriz formatada com PrettyTable.

    Parâmetros:
    ----------
    - mat (list): A matriz a ser impressa.
    - headers (str): Cabeçalho opcional para a tabela.
    - transpose (bool): Se True, transpõe a matriz antes de imprimir.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> matriz = [[1, 2], [3, 4], [5, 6]]
    >>> printMatrizNN(matriz, headers='A B', transpose=False)
    +---+---+
    | A | B |
    +---+---+
    | 1 | 2 |
    | 3 | 4 |
    | 5 | 6 |
    +---+---+

    Nota:
    -----
    Esta função utiliza a biblioteca PrettyTable para formatar a matriz para impressão.
    """
        
    data=mat
    
    table = PrettyTable()
    
    if headers == '':
        table.header = False
        
    elif headers != '':
        table.field_names = headers
        
    if transpose:
        data = mat_transpose(mat)    


    for linha in data:
        table.add_row(linha)
            
    print(table)    
    
def printVetor(list_: list):
    """
    Imprime um vetor formatado.

    Parâmetros:
    ----------
    - list_ (list): O vetor a ser impresso.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> vetor = [1, 2, 3]
    >>> printVetor(vetor)
    [1, 2, 3]
    """

    print('[', end='')
    for i in range(len(list_)):
        if i != len(list_) - 1:
            print(f'{list_[i]}, ', end='')
        else:
            print(f'{list_[i]}', end='')
    print(']')

def separador (matriz: list, tag):
    """
    Insere um separador e uma tag em uma matriz.

    Parâmetros:
    ----------
    - matriz (list): A matriz a ser modificada.
    - tag: A tag a ser inserida.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> matriz = [[1, 2], [3, 4]]
    >>> separador(matriz, "Separação")
    >>> printMatrizNN(matriz)
    +---+---+
    | 1 | 2 |
    | 3 | 4 |
    +---+---+
    | Separação |
    +-----------+
    """
    
    linhaVazia = [''] * 10
    
    matriz.append(linhaVazia)
    matriz.append(tag)
    matriz.append(linhaVazia)

def insereMudancaLinha (matriz: list, linhas: tuple):
    """
    Insere uma mensagem de mudança de linha em uma matriz.

    Parâmetros:
    ----------
    - matriz (list): A matriz a ser modificada.
    - linhas (tuple): As linhas que foram trocadas.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> matriz = [[1, 2], [3, 4]]
    >>> insereMudancaLinha(matriz, (1, 2))
    >>> printMatrizNN(matriz)
    +---+---+
    | 1 | 2 |
    | 3 | 4 |
    +---+---+
    | A linha 1 trocou de lugar com a linha 2   (1, 2) |
    +--------------------------------------------------+
    """
 
    linhaVazia = [''] * 10
    #refatorar
    
    texto = ['A linha {} trocou de lugar com a linha {}   {}'.format(linhas[0], linhas[1], linhas)]
    
    matriz.append(linhaVazia)
    matriz.append (texto)
    matriz.append(linhaVazia)

def mat_transpose(mat: list, method='np'):
    """
    Transpõe uma matriz.

    Parâmetros:
    ----------
    - mat (list): A matriz a ser transposta.
    - method (str): O método de transposição a ser utilizado ('np', 'map', 'zip').

    Retorno:
    --------
    - list: A matriz transposta.

    Exemplo:
    --------
    >>> matriz = [[1, 2], [3, 4], [5, 6]]
    >>> mat_transpose(matriz)
    [[1, 3, 5], [2, 4, 6]]

    Nota:
    -----
    Esta função suporta diferentes métodos de transposição: 'np' (usando numpy), 'map' e 'zip'.
    """
    
    match method:
        case 'np':
            return (np.array(mat, dtype='object').T).tolist()
        
        case 'map':
            return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        
        case 'zip':
            return list(map(list, zip(*mat)))


# ====================== #
#  Operações Matriciais  #
# ====================== #
     
     
def mult_matrizes(matriz1, matriz2):
    """
    Multiplica duas matrizes.

    Parâmetros:
    ----------
    - matriz1 (list): A primeira matriz a ser multiplicada.
    - matriz2 (list): A segunda matriz a ser multiplicada.

    Retorno:
    --------
    - list: O resultado da multiplicação das matrizes.

    Exemplo:
    --------
    >>> matriz1 = [[1, 2], [3, 4]]
    >>> matriz2 = [[1, 0], [0, 1]]
    >>> mult_matrizes(matriz1, matriz2)
    [[1, 2], [3, 4]]

    Levanta:
    --------
    - ValueError: Se o número de colunas da matriz1 for diferente do número de linhas da matriz2.
    """
    
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("O número de colunas da matriz 1 deve ser igual ao número de linhas da matriz 2.")
    
    
    result = [[0 for _ in range(len(matriz2[0]))] for _ in range(len(matriz1))]
    
    
    for i in range(len(matriz1)): 
        for j in range(len(matriz2[0])): 
            for k in range(len(matriz2)): 
                
                result[i][j] += matriz1[i][k] * matriz2[k][j] 
    
    return result


# ===================== #
#  Funções matemáticas  #
# ===================== #

def round_nf(number=None, d_places=0, method='default', alt='default'):
    """
    Arredonda um número para um número especificado de casas decimais.

    Parâmetros:
    ----------
    - number (float): O número a ser arredondado.
    - d_places (int): O número de casas decimais para arredondar.
    - method (str): O método de arredondamento a ser utilizado ('default', 'trunc', 'noround').
    - alt (str): Modo alternativo de retorno de valor arredondado ('default', 'exib').

    Retorno:
    --------
    - float: O número arredondado.

    Exemplo:
    --------
    >>> round_nf(3.14159, 2)
    3.14
    """

    if alt == 'exib':
        return number, round_nf(number, d_places, method=method)
        
                
    elif alt =='default':
        match method:
            case 'default':
                return round(number, d_places)
            
            case '':
                return round(number, d_places)
            
            case 'trunc':
                
                if d_places == 0:
                    return int(number)
                
                return float( str(number)[:str(number).find('.') + d_places+1] )
            case 'noround':
                return number
            
            case _:
                raise ValueError(f"Unknown rounding method: {method}")

def count_d_places(number):
    """
    Conta o número de casas decimais de um número.

    Parâmetros:
    ----------
    - number (float): O número do qual as casas decimais serão contadas.

    Retorno:
    --------
    - int: O número de casas decimais.

    Exemplo:
    --------
    >>> count_d_places(3.14159)
    5
    """

    number_str = str(number)
    
    # Verificando se o número tem uma parte decimal
    if '.' in number_str:
        # Contando os caracteres após o ponto decimal
        return len(number_str.split('.')[1])
    else:
        # Se não há parte decimal, retorna 0
        return 0


# ===================== #
#  Funções de arquvios  #
# ===================== #


def createFile(dataFrame: pd.DataFrame, file_name, file_path='./', index=False):
    """
    Cria um arquivo Excel a partir de um DataFrame do pandas.

    Parâmetros:
    ----------
    - dataFrame (pd.DataFrame): O DataFrame a ser exportado para o Excel.
    - file_name (str): O nome do arquivo Excel.
    - file_path (str): O caminho onde o arquivo será salvo.
    - index (bool): Se True, inclui o índice do DataFrame no arquivo Excel.

    Retorno:
    --------
    - bool: True se o arquivo foi criado com sucesso, False caso contrário.

    Exemplo:
    --------
    >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> createFile(df, 'output', './')
    True
    """
    complete_name = file_path + file_name + '.xlsx'
    try:    
        dataFrame.to_excel(complete_name, engine='openpyxl', index=index)
        return True
        
    except PermissionError as e:
        error_message = str(e)
        
        if 'file is being used by another process' in error_message or 'Permission denied' in error_message:
            print(f'\n\n AVISO: Permissão negada para sobrescrever o arquivo : \'{complete_name}\'.')
            print('Verifique se o arquivo que está tentando criar já existe e está sendo utilizado por outro programa.')
            print('Se não for o caso verifique se essa pasta foi definida com workspace trust, ', end='')
            print ('para garantir que tem permissão para modificar arquivos.\n')
            print(f'** Erro retornado: {error_message}  **\n\n')
        
            print('Opções:')
            print('1. Escolher um nome de arquivo diferente.')
            print('2. Confirmar a substituição do arquivo existente (caso o arquivo não esteja mais sendo utilizado).')
            print('3. Cancelar a operação.')
            escolha = input('\nDigite o número da opção desejada: ')
                  
            if escolha == '1':
                novo_nome = input('Digite um novo nome de arquivo sem extensões: ')
                createFile(dataFrame, (novo_nome + '.xlsx'), index=index)
                
                return True
                
            elif escolha == '2':
                createFile(dataFrame, file_name, index=index)
                
                return True
            
            elif escolha == '3':
                         
                return False
            else:
                print('\nOpção inválida. Tente novamente.')
  
def export_to_excel(mat, path='./', caption=None, transpose = False, headers=None, file_name='test-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
    """
    Exporta uma matriz para um arquivo Excel.

    Parâmetros:
    ----------
    - mat (list): A matriz a ser exportada.
    - path (str): O caminho onde o arquivo será salvo.
    - caption (str): Legenda opcional para o arquivo Excel.
    - transpose (bool): Se True, transpõe a matriz antes da exportação.
    - headers (list): Cabeçalhos personalizados para as colunas.
    - file_name (str): O nome do arquivo Excel.

    Retorno:
    --------
    - bool: True se o arquivo foi exportado com sucesso, False caso contrário.

    Exemplo:
    --------
    >>> matriz = [[1, 2], [3, 4]]
    >>> export_to_excel(matriz, path='./', caption='Dados de exemplo', transpose=False, headers=['A', 'B'], file_name='output')
    True
    """
    if not verify_dependencies(NUMERIC_DEPENDENCIES):
        return  # Alguma dependência está faltando, então a função termina aqui
    
    if transpose:
        df = pd.DataFrame(mat).T
    else:
        df = pd.DataFrame(mat)
        
    # Definir cabeçalhos personalizados se fornecidos
    if headers is not None:
        df.columns = headers
    
    # Se uma legenda foi fornecida, aplicar estilo e definir a legenda
    if caption:
        styler = df.style
        if caption:
            styler = styler.set_caption(caption)

        styler = styler.set_properties(**{'text-align': 'center'})
        
        
    
    # Exportação do DataFrame para um arquivo Excel
    while True:
        
        try:
            if caption:
                return createFile(styler, file_name, path)
            elif not caption:
                return createFile(df, file_name, path)

            break
        
        except Exception as e:
            
            print(f'\nErro ao salvar o arquivo: {e}')
            input('\nNão é possível sobrescrever o arquivo! Feche o arquivo caso esteja aberto e tente novamente...\n')
    
    pass


# ================ #
#  Plot Functions  #
# ================ #

def plot_2d_function_tlwa(y, y_prime, x_points, y_points, directions=True, show_lines=False, length=0.75, x_margin=0):
    """
    Descrição:
    ----------
    Esta função plota uma função bidimensional, juntamente com pontos especificados em x e y. Ela permite traçar retas tangentes à curva 
    a partir dos pontos fornecidos e mostra a diferença em y entre o ponto dado e a curva para comparação de dados obtidos numericamente 
    e uma função analítica.

    Parâmetros:
    -----------
    - y: função
        - A função bidimensional a ser plotada.
    - y_prime: função
        - A derivada da função bidimensional.
    - x_points: array-like
        - Os pontos x dos quais deseja-se traçar as tangentes.
    - y_points: array-like
        - Os valores y correspondentes aos pontos x, onde deseja-se traçar as tangentes.
    - directions: bool (opcional, padrão=True)
        - Indica se as direções das tangentes devem ser mostradas ou não.
    - show_lines: bool (opcional, padrão=False)
        - Indica se as linhas verticais até a curva devem ser mostradas ou não.
    - length: float (opcional, padrão=0.75)
        - O comprimento das setas que representam as tangentes.
    - x_margin: float (opcional, padrão=0)
        - A margem adicional adicionada aos limites dos valores x ao plotar a curva.

    Exemplo:
    --------
    >>> y = lambda x: np.sin(x) + np.cos(x)
    >>> y_prime = lambda x: np.cos(x) - np.sin(x)
    >>> x_points = [1, 2, 3, 4]
    >>> y_points = [y(x) for x in x_points]
    >>> plot_2d_function_tlwa(y, y_prime, x_points, y_points)
    """
    x_range = np.linspace(min(x_points)-x_margin, max(x_points)+x_margin, 400)
    y_val = y(x_range)
    
    plt.figure(figsize=(8, 8))
    plt.plot(x_range, y_val, label="y(x)", zorder=1)  # zorder controla a ordem de plotagem
    
    # Calcular os limites de y, incluindo y_points
    y_min, y_max = min(np.min(y_val), np.min(y_points)), max(np.max(y_val), np.max(y_points))
    
    arrow_length = length * (max(x_points) - min(x_points)) / 10
    arrow_head_width = arrow_length / 5
    arrow_head_length = arrow_length / 3
    
    for x_tangent, y_tangent in zip(x_points, y_points):
        slope_tangent = y_prime(x_tangent)
        
        dx = arrow_length / np.sqrt(1 + slope_tangent**2)
        dy = slope_tangent * dx
        
        if directions:
            plt.arrow(x_tangent, y_tangent, dx, dy, head_width=arrow_head_width, head_length=arrow_head_length, fc='black', ec='black', length_includes_head=True, zorder=3)
        
        if show_lines:
            y_curve_at_x = y(x_tangent)  # Valor de y na curva para o x atual
            plt.vlines(x_tangent, ymin=y_tangent, ymax=y_curve_at_x, color='gray', linestyle='--', zorder=2)
    
    plt.scatter(x_points, y_points, color='red', s=50, alpha=0.8, zorder=4)  # Pontos de tangência
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.xlim([min(x_range), max(x_range)])
    plt.ylim([y_min - 1, y_max + 1])
    plt.axis('equal')
    plt.show()

def plot_2d_function_and_compare(ydx, x_range, x_points, y_points, angles, arrow_length=0.2, rad=True):
    """
    Plota uma função 2D e compara com pontos dados e setas direcionais.

    Parâmetros:
    ----------
    - ydx (function): A função a ser plotada.
    - x_range (tuple): O intervalo de valores de x para plotagem.
    - x_points (list): Os valores de x dos pontos dados.
    - y_points (list): Os valores de y dos pontos dados.
    - angles (list): Os ângulos das setas direcionais.
    - arrow_length (float): O comprimento das setas direcionais.
    - rad (bool): Se True, os ângulos estão em radianos; caso contrário, em graus.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> import numpy as np
    >>> def ydx(x): return np.sin(x)
    >>> x_range = (0, 2*np.pi)
    >>> x_points = [np.pi/4, 3*np.pi/4]
    >>> y_points = [ydx(x) for x in x_points]
    >>> angles = [np.pi/3, np.pi/4]
    >>> plot_2d_function_and_compare(ydx, x_range, x_points, y_points, angles)
    """
    x_values = np.linspace(x_range[0], x_range[1], 400)
    y_values = [ydx(x) for x in x_values]

    # Plotar a curva da função
    plt.plot(x_values, y_values, label='Curva da função fdxy', zorder=1)

    # Plotar os pontos dados
    plt.scatter(x_points, y_points, color='red', zorder=5, label='Pontos dados')

    # Para cada ponto e ângulo dados, plotar uma seta com o ângulo dado
    for xi, yi, angle in zip(x_points, y_points, angles):
        # Converter ângulo para radianos se necessário
        angle_rad = angle if rad else np.deg2rad(angle)

        # Calcular o vetor direção normalizado (comprimento 1)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)

        # Normalizar o vetor direção (dx, dy)
        length = np.sqrt(dx**2 + dy**2)
        dx /= length
        dy /= length

        # Plotar a seta com tamanho padrão
        plt.arrow(xi, yi, dx*arrow_length, dy*arrow_length, head_width=0.1, head_length=0.1, fc='black', ec='black', zorder=4)

        # Plotar a linha vertical pontilhada do ponto dado até a curva
        yi_true = ydx(xi)
        plt.vlines(xi, yi, yi_true, color='black', linestyles='dashed', zorder=4)

    # Adicionar legendas e títulos
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Comparação entre a função fdxy e pontos dados com setas em ângulos definidos')
    plt.legend()

    # Exibir o gráfico
    plt.show()

def plot_3d_function_and_arrows(ydx, x_range, y_range, x_points, y_points, z_points, angles, arrow_length=0.2, rad=True):
    """
    Plota uma função 3D e setas direcionais.

    Parâmetros:
    ----------
    - ydx (function): A função a ser plotada.
    - x_range (tuple): O intervalo de valores de x para plotagem.
    - y_range (tuple): O intervalo de valores de y para plotagem.
    - x_points (list): Os valores de x dos pontos dados.
    - y_points (list): Os valores de y dos pontos dados.
    - z_points (list): Os valores de z dos pontos dados.
    - angles (list): Os ângulos das setas direcionais.
    - arrow_length (float): O comprimento das setas direcionais.
    - rad (bool): Se True, os ângulos estão em radianos; caso contrário, em graus.

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> import numpy as np
    >>> def ydx(x, y): return np.sin(x) + np.cos(y)
    >>> x_range = (0, 2*np.pi)
    >>> y_range = (0, 2*np.pi)
    >>> x_points = [np.pi/4, 3*np.pi/4]
    >>> y_points = [np.pi/6, np.pi/3]
    >>> z_points = [ydx(x, y) for x, y in zip(x_points, y_points)]
    >>> angles = [np.pi/3, np.pi/4]
    >>> plot_3d_function_and_arrows(ydx, x_range, y_range, x_points, y_points, z_points, angles)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Gera uma grade de valores para x e y
    x_values = np.linspace(x_range[0], x_range[1], 400)
    y_values = np.linspace(y_range[0], y_range[1], 400)
    x_grid, y_grid = np.meshgrid(x_values, y_values)

    # Calcula os valores de z com base na função ydx para cada ponto na grade
    z_grid = ydx(x_grid, y_grid)

    # Plotar a superfície
    surf = ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none', alpha=0.7)

    # Para cada ponto e ângulo dados, plotar uma seta
    for xi, yi, zi, angle in zip(x_points, y_points, z_points, angles):
        # Converter ângulo para radianos se necessário
        angle_rad = angle if rad else np.deg2rad(angle)

        # Calcular o vetor direção normalizado (comprimento 1)
        u = np.cos(angle_rad) * arrow_length
        v = np.sin(angle_rad) * arrow_length
        w = 0  # Sem componente vertical para as setas

        # Plotar a seta usando quiver
        ax.quiver(xi, yi, zi, u, v, w, length=arrow_length, arrow_length_ratio=0.1, color='black')

    # Adicionar legendas e títulos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gráfico 3D da função ydx e setas direcionais')

    # Exibir o gráfico
    plt.show()
    
    
def plot_and_compare(ydx, x_range, x_points, y_points, angles, arrow_length=0.2, rad=True, y_range = None, z_points = None):
    """
    Plota uma função e compara com pontos dados e setas direcionais.

    Parâmetros:
    ----------
    - ydx (function): A função a ser plotada.
    - x_range (tuple): O intervalo de valores de x para plotagem.
    - x_points (list): Os valores de x dos pontos dados.
    - y_points (list): Os valores de y dos pontos dados.
    - angles (list): Os ângulos das setas direcionais.
    - arrow_length (float): O comprimento das setas direcionais.
    - rad (bool): Se True, os ângulos estão em radianos; caso contrário, em graus.
    - y_range (tuple): O intervalo de valores de y para plotagem (para funções 3D).
    - z_points (list): Os valores de z dos pontos dados (para funções 3D).

    Retorno:
    --------
    - None

    Exemplo:
    --------
    >>> import numpy as np
    >>> def ydx(x): return np.sin(x)
    >>> x_range = (0, 2*np.pi)
    >>> x_points = [np.pi/4, 3*np.pi/4]
    >>> y_points = [ydx(x) for x in x_points]
    >>> angles = [np.pi/3, np.pi/4]
    >>> plot_and_compare(ydx, x_range, x_points, y_points, angles)
    """
    if get_number_of_arguments(ydx) == 1:
        return plot_2d_function_and_compare(ydx = ydx,
                                           x_range = x_range, 
                                           x_points = x_points,
                                           y_points = y_points,
                                           angles = angles,
                                           arrow_length=arrow_length,
                                           rad=rad
        )
    elif get_number_of_arguments(ydx) == 2:
        return plot_3d_function_and_arrows(ydx = ydx,
                                           x_range = x_range, 
                                           y_range = y_range,
                                           x_points = x_points,
                                           y_points = y_points,
                                           z_points = z_points,
                                           angles = angles,
                                           arrow_length=arrow_length,
                                           rad=rad
        )
    
    return print ('Função inválida utilziada')

def get_number_of_arguments(func):
    """
    Retorna o número de argumentos de uma função.

    Parâmetros:
    ----------
    - func (callable): A função para a qual o número de argumentos será calculado.

    Retorno:
    --------
    - int: O número de argumentos da função.

    Exemplo:
    --------
    >>> def func(a, b, c):
    ...     pass
    >>> get_number_of_arguments(func)
    3
    """
    sig = inspect.signature(func)
    return len(sig.parameters)


if __name__ == '__main__':
    pass