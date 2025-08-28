import csv


def write_to_csv_file(name, text, user_name, user_id, date):
    with open(name, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([user_name, date, text, user_id])


def reader_to_csv_file(name_csv):
    with open(name_csv, newline='', encoding='utf-8', mode='r') as f:
        reader = csv.reader(f, delimiter=';')
        return [row for row in reader][::-1]


def create_format(row):
    return f"{row[0]} | {row[1]} | {row[2]}"
