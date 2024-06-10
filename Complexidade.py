# Lista de elementos
main = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','z']

# Função para gerar combinações
def generate_combinations(elements, size):
    n = len(elements)
    indices = list(range(size))  # Inicia com os primeiros 'size' índices
    while True:
        # Cria a combinação atual baseada nos índices
        yield [elements[i] for i in indices]
        
        # Encontra o índice que precisa ser incrementado
        for i in reversed(range(size)):
            if indices[i] != i + n - size:
                break
        else:
            return  # Todos os índices foram percorridos, termina a iteração
        
        # Incrementa o índice encontrado
        indices[i] += 1
        
        # Ajusta os índices seguintes
        for j in range(i + 1, size):
            indices[j] = indices[j - 1] + 1

# Função para gerar combinações e salvar em listas
def generate_combinations_in_lists(elements, start_size, end_size):
    all_combinations = {}
    for size in range(start_size, end_size + 1):
        all_combinations[size] = list(generate_combinations(elements, size))
    return all_combinations

# Gera combinações para tamanhos de 10 a 15
combinations_dict = generate_combinations_in_lists(main, 10, 15)

# Acessando as combinações de cada tamanho
combinations_10 = combinations_dict[10]
combinations_11 = combinations_dict[11]
combinations_12 = combinations_dict[12]
combinations_13 = combinations_dict[13]
combinations_14 = combinations_dict[14]
combinations_15 = combinations_dict[15]

# Exemplo de uso: imprimir a quantidade de combinações de cada tamanho
for size in range(10, 16):
    print(f"Total de combinações com {size} elementos: {len(combinations_dict[size])}")
