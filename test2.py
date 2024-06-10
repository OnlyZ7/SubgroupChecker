import multiprocessing
from itertools import combinations

main = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','z']

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
def find_subsets_parallel(combinations_14, combinations_15):
    found_subsets = []

    print("Iniciando a verificação de subconjuntos...")

    while combinations_14:
        max_elimina = 0
        melhor_subconjunto = None
        
        # Paraleliza a verificação de subconjuntos
        with multiprocessing.Pool() as pool:
            results = pool.map(is_subset_wrapper, [(combo_14, combo_15) for combo_14 in combinations_14 for combo_15 in combinations_15])
        
        elimina_count = {}
        for idx, (combo_14, combo_15) in enumerate([(combo_14, combo_15) for combo_14 in combinations_14 for combo_15 in combinations_15]):
            if results[idx]:
                if combo_15 not in elimina_count:
                    elimina_count[combo_15] = 0
                elimina_count[combo_15] += 1

        if elimina_count:
            melhor_subconjunto = max(elimina_count, key=elimina_count.get)
            max_elimina = elimina_count[melhor_subconjunto]

        if melhor_subconjunto is not None:
            found_subsets.append(melhor_subconjunto)
            combinations_14 = [combo_14 for combo_14 in combinations_14 if not is_subset(combo_14, melhor_subconjunto)]
            combinations_15.remove(melhor_subconjunto)

    return found_subsets

if __name__ == '__main__':
    # Gera combinações para tamanhos de 14 e 15
    print("Gerando combinações...")
    combinations_dict = generate_combinations_in_lists(main, 14, 15)

    # Acessando as combinações de cada tamanho
    combinations_14 = combinations_dict[14]
    combinations_15 = combinations_dict[15]

    print("Combinações geradas.")
    print(f"Total de combinações com 14 elementos: {len(combinations_14)}")
    print(f"Total de combinações com 15 elementos: {len(combinations_15)}")

    # Encontra as combinações de 14 elementos que estão presentes em combinações de 15 elementos
    found_combinations_14_in_15 = find_subsets_parallel(combinations_14, combinations_15)

    # Imprime a quantidade de combinações encontradas
    print("\nQuantidade de combinações de 14 elementos encontradas em combinações de 15 elementos:", len(found_combinations_14_in_15))