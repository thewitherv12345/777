import subprocess


def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    return result.stdout.strip()

def get_local_changes(only_new=False):
    output = run_git_command(["status", "--short"])

    lines = output.split("\n")
    print("Локальные изменения:" if not only_new else "Только новые локальные файлы:")
    changed_count = 0

    for line in lines:
        if line.strip():
            status = line[:2].strip()
            file_path = line[3:].strip()

            if only_new and status not in ['??', 'A']:
                continue

            print(line)
            changed_count += 1

    print(f"Количество локальных изменений: {changed_count}")


if __name__ == "__main__":
    get_local_changes()

    get_local_changes(only_new=True)
