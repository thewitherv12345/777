import subprocess
import csv


def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    return result.stdout.strip()

def get_local_changes(only_new=False, csv_filename="changes.csv"):
    output = run_git_command(["status", "--short"])
    lines = output.split("\n")

    changes = []
    for line in lines:
        if not line.strip():
            continue

        status = line[:2].strip()
        filename = line[3:].strip()

        if only_new and status not in ["??", "A"]:
            continue

        changes.append((status, filename))

    mode = "a" if only_new else "w"  # Перезаписываем при первом вызове
    with open(csv_filename, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(["Status", "File"])
        writer.writerows(changes)

    print("Изменения:" if not only_new else "Новые файлы:")
    for status, filename in changes:
        print(f"{status}\t{filename}")

    print(f"Количество  изменений: {len(changes)}")


if __name__ == "__main__":
    get_local_changes(False)
    get_local_changes(True)
