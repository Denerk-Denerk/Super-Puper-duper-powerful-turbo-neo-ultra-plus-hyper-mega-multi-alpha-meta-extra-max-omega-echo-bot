import csv


def write_to_csv_file(name, text, user_name, user_id, date, message_id):
    with open(name, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([user_name, date, text, user_id, message_id])

def write_to_csv_stat(name, stats):
    with open(name, 'w', encoding='utf8', newline='') as f:
        fieldnames = ['username', 'stat', 'last_message_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for stat in stats:
            data = [{'username': stat[0], 'stat': stat[1], 'last_message_id': stat[2]}]
            writer.writerows(data)



def reader_to_csv_file(name_csv):
    with open(name_csv, newline='', encoding='utf-8', mode='r') as f:
        reader = csv.DictReader(f, delimiter=';')
        return [row for row in reader][::-1]



def create_format(row):
    return f"{row['username']} | {row['date']} | {row['text']}"
