import subprocess


def run_git_command(args):
    """Вспомогательная функция для запуска Git-команд с обработкой ошибок."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ошибка при выполнении команды Git: {result.stderr.strip()}")
        print("Убедитесь, что вы в Git-репозитории, Git установлен, и remote настроен.")
        return None
    return result.stdout.strip()


def get_local_changes(only_new=False):
    """Проверяет локальные изменения (как в исходном скрипте)."""
    output = run_git_command(["status", "--short"])
    if output is None:
        return

    lines = output.split("\n")
    print("Локальные изменения:" if not only_new else "Только новые локальные файлы:")
    changed_count = 0

    for line in lines:
        if line.strip():
            status = line[:2].strip()
            file_path = line[3:].strip()

            # Фильтр по .py (можно убрать)
            if not file_path.endswith('.py'):
                continue

            # Фильтр только новых
            if only_new and status not in ['??', 'A']:
                continue

            print(line)
            changed_count += 1

    print(f"Количество локальных изменений: {changed_count}")


def get_remote_changes(only_new=False, branch="main"):
    """Проверяет изменения на удалённом репозитории по сравнению с локальным."""
    # Сначала fetch, чтобы обновить данные о remote
    run_git_command(["fetch"])

    # Получаем diff с remote веткой
    output = run_git_command(["diff", "--name-status", "HEAD", f"origin/{branch}"])
    if output is None:
        return

    lines = output.split("\n")
    print("Изменения на remote (по сравнению с локальным):" if not only_new else "Только новые файлы на remote:")
    changed_count = 0

    for line in lines:
        if line.strip():
            status = line[0]  # Статус: A (added), M (modified), D (deleted), etc.
            file_path = line[1:].strip()

            # Фильтр по .py (можно убрать)
            if not file_path.endswith('.py'):
                continue

            # Фильтр только новых (added on remote)
            if only_new and status != 'A':
                continue

            print(f"{status}\t{file_path}")
            changed_count += 1

    print(f"Количество изменений на remote: {changed_count}")

    # Дополнительно: Проверяем статус ветки
    status_output = run_git_command(["status"])
    if status_output:
        print("\nСтатус ветки относительно remote:")
        for line in status_output.split("\n"):
            if "Your branch" in line:
                print(line)


if __name__ == "__main__":
    # Локальные изменения
    get_local_changes()
    print("\nТолько новые локальные файлы:")
    get_local_changes(only_new=True)

    # Изменения на remote
    print("\n--- Проверка remote ---")
    get_remote_changes()
    print("\nТолько новые файлы на remote:")
    get_remote_changes(only_new=True)