import re

# Especifique o caminho absoluto para o arquivo de entrada
file_path = rf"C:\Users\guilhermemachancoses\Documents\GitHub\Python-Programs\dados.txt"

# Abrir o arquivo txt de entrada usando o caminho absoluto
with open(file_path, 'r') as file:
    # Ler todas as linhas do arquivo
    lines = file.readlines()

# Expressão regular para encontrar as informações de 'firstname' e 'lastname'
pattern = rf"INSERT INTO `users` \(`users_id`, `firstname`, `lastname`,"

# Lista para armazenar os dados formatados
formatted_data = []

# Iterar sobre as linhas e encontrar os nomes
for line in lines:
    match = re.match(pattern, line)
    if match:
        firstname = match.group(2).capitalize()
        lastname = match.group(3).capitalize()
        formatted_data.append(f"'{firstname}', '{lastname}'")
    else:
        print("Linha não corresponde ao padrão regex:")
        print(line)

# Especifique o caminho absoluto para o arquivo de saída
output_file_path = rf"C:\Users\guilhermemachancoses\Documents\GitHub\Python-Programs\alterado.txt"

# Escrever os dados formatados no novo arquivo "alterado.txt" usando o caminho absoluto
with open(output_file_path, 'w') as output_file:
    for data in formatted_data:
        output_file.write(data + '\n')
