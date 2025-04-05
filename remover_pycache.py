import os
import shutil

def find_duplicates(base_dir, target_name):
    """Encontra arquivos com o mesmo nome em diferentes diretórios."""
    duplicates = []
    for root, _, files in os.walk(base_dir):
        if target_name in files:
            duplicates.append(os.path.join(root, target_name))
    return duplicates

def remove_pycache(base_dir):
    """Remove todos os diretórios __pycache__ e arquivos .pyc."""
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith(".pyc"):
                os.remove(os.path.join(root, file_name))

def resolve_test_mismatch(base_dir, test_file_name):
    """Corrige o problema de arquivos de teste duplicados."""
    duplicates = find_duplicates(base_dir, test_file_name)

    if len(duplicates) > 1:
        print(f"Encontrados arquivos duplicados para {test_file_name}:")
        for file in duplicates:
            print(f" - {file}")

        print("\nRemovendo duplicatas desnecessárias...")
        # Mantém apenas o arquivo na pasta `tests`
        for file in duplicates:
            if not file.startswith(os.path.join(base_dir, "tests")):
                print(f"Removendo: {file}")
                os.remove(file)

    else:
        print(f"Nenhum arquivo duplicado encontrado para {test_file_name}.")

    print("\nLimpando __pycache__ e arquivos .pyc...")
    remove_pycache(base_dir)
    print("Limpeza concluída.")

if __name__ == "__main__":
    BASE_DIR = os.getcwd()  # Diretório base
    TEST_FILE_NAME = "test_cadastro_validations.py"

    print(f"Iniciando correção para {TEST_FILE_NAME} no diretório {BASE_DIR}...\n")
    resolve_test_mismatch(BASE_DIR, TEST_FILE_NAME)
    print("\nCorreção concluída!")
