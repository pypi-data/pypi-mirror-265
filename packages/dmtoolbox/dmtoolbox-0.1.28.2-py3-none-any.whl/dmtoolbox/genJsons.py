
import os
import json
import re

    
# Functions
__all__ = ['file_to_json', 'save_json_to_json_file', 'update_variable_declaration_in_script']

# Variables
__all__ += []



def file_to_json(file_path):
    """
    Lê o conteúdo de um arquivo JSON e retorna como um objeto Python.

    Parâmetros:
    -----------
    - file_path: str
        - O caminho do arquivo JSON a ser lido.

    Retorno:
    --------
    - dict ou list
        - O conteúdo do arquivo JSON convertido em um objeto Python (dicionário ou lista).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

def save_json_to_json_file(json_content, file_path):
    """
    Salva o conteúdo de um objeto Python (dicionário ou lista) como um arquivo JSON.

    Parâmetros:
    -----------
    - json_content: dict ou list
        - O conteúdo a ser salvo como JSON.
    - file_path: str
        - O caminho onde o arquivo JSON será salvo.

    Nota:
    -----
    Esta função usa 'json.dump' para converter o objeto Python em JSON e salvá-lo no arquivo especificado.
    """
    # Garantindo que o diretório onde o arquivo será salvo existe
    os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # json.dump é usado para converter o objeto Python (dicionário ou lista) em JSON e salvar no arquivo
            json.dump(json_content, file, indent=4, ensure_ascii=False)
        print(f"Arquivo JSON salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

def update_variable_declaration_in_script(file_path, script_path, variable_name):
    """
    Atualiza a declaração de uma variável em um script Python com o conteúdo de um arquivo JSON.

    Parâmetros:
    -----------
    - file_path: str
        - O caminho do arquivo JSON que contém o conteúdo a ser inserido no script.
    - script_path: str
        - O caminho do script Python onde a declaração da variável será atualizada.
    - variable_name: str
        - O nome da variável no script a ser atualizada.

    Nota:
    -----
    Esta função lê o conteúdo do arquivo JSON especificado e prepara uma nova declaração de variável
    com esse conteúdo. Em seguida, ela substitui a declaração existente da variável no script
    pelo novo conteúdo preparado.
    """
    try:
        # Abre o arquivo que contém a string JSON e lê seu conteúdo
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo '{file_path}': {e}")
        return

    # Prepara o novo conteúdo a ser inserido no script de destino
    new_declaration = f'{variable_name} = {content}\n'

    try:
        with open(script_path, 'r', encoding='utf-8') as original_script:
            lines = original_script.readlines()

        # Substitui a declaração da variável no script
        updated_lines = []
        variable_pattern = re.compile(f'^{variable_name} =')
        for line in lines:
            if variable_pattern.match(line):
                updated_lines.append(new_declaration)
            else:
                updated_lines.append(line)

        with open(script_path, 'w', encoding='utf-8') as modified_script:
            modified_script.writelines(updated_lines)

        print(f"Declaração da variável '{variable_name}' atualizada com sucesso no script '{script_path}'.")
    except FileNotFoundError:
        print(f"Erro: Script de destino '{script_path}' não encontrado.")
    except Exception as e:
        print(f"Erro ao modificar o script '{script_path}': {e}")


    
if __name__ == '__main__':
    pass
