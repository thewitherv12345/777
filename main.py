import subprocess
import csv

csv_filename="changes.csv"

def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    return result.stdout.strip()

def get_local_changes():
    output = run_git_command(["status", "--short"])
    lines = output.split("\n")

    changes = []
    for line in lines:
        if not line.strip():
            continue

        status = line[:2].strip()
        filename = line[3:].strip()

        if status not in ["??", "A"]:
            continue

        changes.append((status, filename))

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Status", "File"])
        writer.writerows(changes)

    print("Новые файлы: ")
    for status, filename in changes:
        print(f"{status}\t{filename}")

    print(f"Количество  изменений: {len(changes)}")


if __name__ == "__main__":
    get_local_changes()
