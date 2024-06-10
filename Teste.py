import multiprocessing
from itertools import combinations

main = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

# Função para gerar combinações
def generate_combinations(elements, size):
    return list(combinations(elements, size))

# Função para gerar combinações e salvar em listas
def generate_combinations_in_lists(elements, start_size, end_size):
    all_combinations = {}
    for size in range(start_size, end_size + 1):
        print(f"Gerando combinações de tamanho {size}...")
        all_combinations[size] = generate_combinations(elements, size)
        print(f"Total de combinações com {size} elementos: {len(all_combinations[size])}")
    return all_combinations

# Função para verificar se uma lista está contida em outra
def is_subset(subset, superset):
    return all(elem in superset for elem in subset)

# Função auxiliar para permitir uso de is_subset com pool.map
def is_subset_wrapper(args):
    subset, superset = args
    return is_subset(subset, superset)

# Função para encontrar os subconjuntos usando multiprocessamento
def find_subsets_parallel(combinations_5, combinations_6):
    found_subsets = []

    print("Iniciando a verificação de subconjuntos...")

    while combinations_5:
        max_elimina = 0
        melhor_subconjunto = None
        
        # Paraleliza a verificação de subconjuntos
        with multiprocessing.Pool() as pool:
            results = pool.map(is_subset_wrapper, [(combo_5, combo_6) for combo_5 in combinations_5 for combo_6 in combinations_6])
        
        elimina_count = {}
        for idx, (combo_5, combo_6) in enumerate([(combo_5, combo_6) for combo_5 in combinations_5 for combo_6 in combinations_6]):
            if results[idx]:
                if combo_6 not in elimina_count:
                    elimina_count[combo_6] = 0
                elimina_count[combo_6] += 1

        if elimina_count:
            melhor_subconjunto = max(elimina_count, key=elimina_count.get)
            max_elimina = elimina_count[melhor_subconjunto]

        if melhor_subconjunto is not None:
            found_subsets.append(melhor_subconjunto)
            combinations_5 = [combo_5 for combo_5 in combinations_5 if not is_subset(combo_5, melhor_subconjunto)]
            combinations_6.remove(melhor_subconjunto)

    return found_subsets

if __name__ == '__main__':
    # Gera combinações para tamanhos de 5 e 6
    print("Gerando combinações...")
    combinations_dict = generate_combinations_in_lists(main, 5, 6)

    # Acessando as combinações de cada tamanho
    combinations_5 = combinations_dict[5]
    combinations_6 = combinations_dict[6]

    print("Combinações geradas.")
    print(f"Total de combinações com 5 elementos: {len(combinations_5)}")
    print(f"Total de combinações com 6 elementos: {len(combinations_6)}")

    # Imprimir os conjuntos de 5 e 6 elementos
    print("\nConjuntos de 5 elementos:")
    for combo in combinations_5:
        print(combo)

    print("\nConjuntos de 6 elementos:")
    for combo in combinations_6:
        print(combo)

    # Encontra as combinações de 5 elementos que estão presentes em combinações de 6 elementos
    found_combinations_5_in_6 = find_subsets_parallel(combinations_5, combinations_6)

    # Imprime a quantidade de combinações encontradas
    print("\nQuantidade de combinações de 5 elementos encontradas em combinações de 6 elementos:", len(found_combinations_5_in_6))
