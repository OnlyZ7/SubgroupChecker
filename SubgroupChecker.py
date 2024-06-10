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
def find_subsets_parallel(combinations_small, combinations_large, batch_size=100, num_processes=1):
    found_subsets = []

    print("Iniciando a verificação de subconjuntos...")

    while combinations_small:
        max_elimina = 0
        melhor_subconjunto = None

        # Divida as combinações de tamanho maior em lotes menores
        for i in range(0, len(combinations_large), batch_size):
            batch_combinations_large = combinations_large[i:i + batch_size]

            # Paraleliza a verificação de subconjuntos
            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.map(is_subset_wrapper, [(combo_small, combo_large) for combo_small in combinations_small for combo_large in batch_combinations_large])

            elimina_count = {}
            for idx, (combo_small, combo_large) in enumerate([(combo_small, combo_large) for combo_small in combinations_small for combo_large in batch_combinations_large]):
                if results[idx]:
                    if combo_large not in elimina_count:
                        elimina_count[combo_large] = 0
                    elimina_count[combo_large] += 1

            if elimina_count:
                melhor_subconjunto_batch = max(elimina_count, key=elimina_count.get)
                max_elimina_batch = elimina_count[melhor_subconjunto_batch]

                if max_elimina_batch > max_elimina:
                    melhor_subconjunto = melhor_subconjunto_batch
                    max_elimina = max_elimina_batch

        if melhor_subconjunto is not None:
            found_subsets.append(melhor_subconjunto)
            combinations_small = [combo_small for combo_small in combinations_small if not is_subset(combo_small, melhor_subconjunto)]
            combinations_large = [combo_large for combo_large in combinations_large if combo_large != melhor_subconjunto]

    return found_subsets

if __name__ == '__main__':
    # Gera combinações para tamanhos de 10, 11, 12, 13, 14 e 15
    print("Gerando combinações...")
    combinations_dict = generate_combinations_in_lists(main, 10, 15)

    # Acessando as combinações de cada tamanho
    combinations_10 = combinations_dict[10]
    combinations_11 = combinations_dict[11]
    combinations_12 = combinations_dict[12]
    combinations_13 = combinations_dict[13]
    combinations_14 = combinations_dict[14]
    combinations_15 = combinations_dict[15]

    print("Combinações geradas.")
    print(f"Total de combinações com 10 elementos: {len(combinations_10)}")
    print(f"Total de combinações com 11 elementos: {len(combinations_11)}")
    print(f"Total de combinações com 12 elementos: {len(combinations_12)}")
    print(f"Total de combinações com 13 elementos: {len(combinations_13)}")
    print(f"Total de combinações com 14 elementos: {len(combinations_14)}")
    print(f"Total de combinações com 15 elementos: {len(combinations_15)}")

    # Encontra as combinações de tamanhos menores que estão presentes em combinações de tamanhos maiores
    found_combinations_14_in_15 = find_subsets_parallel(combinations_14, combinations_15)
    found_combinations_13_in_15 = find_subsets_parallel(combinations_13, combinations_15)
    found_combinations_12_in_15 = find_subsets_parallel(combinations_12, combinations_15)
    found_combinations_11_in_15 = find_subsets_parallel(combinations_11, combinations_15)
    found_combinations_10_in_15 = find_subsets_parallel(combinations_10, combinations_15)

    # Imprime a quantidade de combinações encontradas
    print("Quantidade de combinações de 14 elementos encontradas em combinações de 15 elementos:", len(found_combinations_14_in_15))
    print("Quantidade de combinações de 13 elementos encontradas em combinações de 15 elementos:", len(found_combinations_13_in_15))
    print("Quantidade de combinações de 12 elementos encontradas em combinações de 15 elementos:", len(found_combinations_12_in_15))
    print("Quantidade de combinações de 11 elementos encontradas em combinações de 15 elementos:", len(found_combinations_11_in_15))
    print("Quantidade de combinações de 10 elementos encontradas em combinações de 15 elementos:", len(found_combinations_10_in_15))
