import yaml


def xor_vector_with_number(vector, number):
    """Выполняет побитовую операцию XOR для каждого элемента вектора с заданным числом."""
    for i in range(len(vector)):
        vector[i] ^= number  # Выполнение XOR
    return vector


def main():
    # Исходный вектор длины 6
    vector = [0, 1, 2, 3, 4, 5]

    # Число для операции XOR
    number = 149  # в бинарной форме это 0b10010101

    # Применяем операцию XOR ко всем элементам вектора
    result_vector = xor_vector_with_number(vector, number)

    # Выводим результат
    print("Результат XOR над вектором:", result_vector)

    # Сохраняем результат в yaml файл
    with open('result.yaml', 'w') as f:
        yaml.dump({'result_vector': result_vector}, f)


if __name__ == "__main__":
    main()
