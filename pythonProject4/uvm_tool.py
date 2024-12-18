import yaml
import struct
import argparse


def assemble(input_path, output_path, log_path):
    """Ассемблирует текстовую программу в бинарный файл и логирует команды в YAML."""
    with open(input_path, 'r') as f:
        lines = f.readlines()

    binary_instructions = []
    log_data = []

    for line in lines:
        command, *args = line.strip().split()
        if command == "LOAD":
            # Пример команды "LOAD constant"
            A = 49  # Код команды
            B = int(args[0])  # Константа

            # Ограничение на 30 бит для B и 6 бит для A
            B = B & 0x3FFFFFFF  # Обрезаем B до 30 бит

            # Формируем инструкцию с ограничением на 32 бита
            instruction = ((A & 0x3F) << 30) | B
            instruction &= 0xFFFFFFFF  # Убедимся, что инструкция не выходит за пределы 32 бит

            binary_instructions.append(instruction)
            log_data.append({'A': A, 'B': B, 'instruction': hex(instruction)})

        elif command == "WRITE":
            # Команда записи
            A = 63  # Код команды
            B = int(args[0])  # Адрес

            # Ограничение на 30 бит для B и 6 бит для A
            B = B & 0x3FFFFFFF  # Обрезаем B до 30 бит

            instruction = ((A & 0x3F) << 30) | B
            instruction &= 0xFFFFFFFF  # Убедимся, что инструкция не выходит за пределы 32 бит

            binary_instructions.append(instruction)
            log_data.append({'A': A, 'B': B, 'instruction': hex(instruction)})

        elif command == "XOR":
            # Команда XOR
            A = 53  # Код команды
            B = int(args[0])  # Адрес

            # Ограничение на 30 бит для B и 6 бит для A
            B = B & 0x3FFFFFFF  # Обрезаем B до 30 бит

            instruction = ((A & 0x3F) << 30) | B
            instruction &= 0xFFFFFFFF  # Убедимся, что инструкция не выходит за пределы 32 бит

            binary_instructions.append(instruction)
            log_data.append({'A': A, 'B': B, 'instruction': hex(instruction)})

    with open(output_path, 'wb') as f:
        for inst in binary_instructions:
            f.write(struct.pack('>I', inst))  # Запись 4 байт на инструкцию

    with open(log_path, 'w') as f:
        yaml.dump(log_data, f)


def interpret(binary_path, memory_dump_path, memory_range):
    """Интерпретирует бинарный файл и сохраняет диапазон памяти в YAML."""
    with open(binary_path, 'rb') as f:
        instructions = f.read()

    accumulator = 0
    memory = [0] * 1024  # Пример памяти размером 1024 слов

    for i in range(0, len(instructions), 5):
        command = instructions[i]
        if command == 0x31:  # Команда LOAD
            B = int.from_bytes(instructions[i + 1:i + 5], 'big')
            accumulator = B
        elif command == 0x63:  # Команда WRITE
            B = int.from_bytes(instructions[i + 1:i + 5], 'big')
            memory[B] = accumulator
        elif command == 0x35:  # Команда XOR
            B = int.from_bytes(instructions[i + 1:i + 5], 'big')
            accumulator ^= memory[B]

    memory_dump = {'memory': memory[memory_range[0]:memory_range[1]]}
    with open(memory_dump_path, 'w') as f:
        yaml.dump(memory_dump, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Ассемблер
    asm_parser = subparsers.add_parser("assemble", help="Run assembler")
    asm_parser.add_argument('--input', required=True, help="Path to input file")
    asm_parser.add_argument('--output', required=True, help="Path to binary output file")
    asm_parser.add_argument('--log', required=True, help="Path to log file")

    # Интерпретатор
    int_parser = subparsers.add_parser("interpret", help="Run interpreter")
    int_parser.add_argument('--binary', required=True, help="Path to binary input file")
    int_parser.add_argument('--memory_dump', required=True, help="Path to memory dump file")
    int_parser.add_argument('--memory_range', nargs=2, type=int, required=True,
                            help="Range of memory to dump (start end)")

    args = parser.parse_args()

    if args.mode == "assemble":
        assemble(args.input, args.output, args.log)
    elif args.mode == "interpret":
        interpret(args.binary, args.memory_dump, args.memory_range)
