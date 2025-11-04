import subprocess

def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    return result.stdout.strip()

def get_local_changes(only_new=False):
    output = run_git_command(["status", "--short"])

    lines = output.split("\n")
    print("Изменения:" if not only_new else "Новые файлы:")
    changed_count = 0

    for line in lines:
        if line.strip():
            status = line[:2].strip()
            if only_new and status not in ['??', 'A']:
                continue

            print(line)
            changed_count += 1

    print(f"Количество изменений: {changed_count}")


if __name__ == "__main__":
    get_local_changes(False)
    get_local_changes(True)
