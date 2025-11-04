import subprocess


def get_changed_files(only_new=False):
    # Выполняем git status --short
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)

    # Проверяем на ошибки (из задания №7)
    if result.returncode != 0:
        print("Ошибка при выполнении команды Git. Убедитесь, что вы в Git-репозитории и Git установлен.")
        return

    # Получаем строки вывода
    lines = result.stdout.strip().split("\n")

    # Фильтруем и выводим
    print("Изменённые файлы:" if not only_new else "Только новые файлы:")
    changed_count = 0  # Подсчёт количества (из задания №4, для полноты)

    for line in lines:
        if line.strip():  # Игнорируем пустые
            status = line[:2].strip()  # Статус: ??, A, M, D и т.д.
            file_path = line[3:].strip()  # Путь к файлу

            # Фильтр по расширению .py (из задания №3, опционально; можно убрать)
            if not file_path.endswith('.py'):
                continue  # Показываем только .py для примера; удалите, если не нужно

            # Фильтр только новых (задание №8)
            if only_new and status not in ['??', 'A']:
                continue  # Пропускаем, если не новый

            print(line)
            changed_count += 1

    # Вывод количества (из задания №4)
    print(f"Количество изменений: {changed_count}")


if __name__ == "__main__":
    # Вызов без параметра (все изменения)
    get_changed_files()

    # Вызов с параметром (только новые)
    print("\nВывод только новых файлов:")
    get_changed_files(only_new=True)