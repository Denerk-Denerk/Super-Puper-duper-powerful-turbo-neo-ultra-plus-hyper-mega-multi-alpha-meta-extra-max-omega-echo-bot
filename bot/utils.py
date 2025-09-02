# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Some utils for easy life
# ----------------------------------------------------------------------

# Python modules
import csv
import datetime
import os
from pathlib import Path

# Custom modules
from settings import FILES_DIR_PATH, STATS_FILE


def abs_path(func):
    def wrapper(*args, **kwargs):
        try:
            fname = kwargs.get("fname")
            path = os.path.join(FILES_DIR_PATH, fname)
            abs_path = Path(path).resolve()
            kwargs["fname"] = abs_path
        except Exception:
            pass
        result = func(*args, **kwargs)
        return result
    return wrapper


@abs_path
def write_to_csv_file(*, fname, data, mode="a"):
    with open(fname, mode=mode, encoding='utf8', newline='') as f:
        fields = list(data)
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')
        writer.writerow(data)


@abs_path
def read_csv_file(*, fname, fields):
    if not os.path.exists(fname):
        return []
    with open(fname, newline='', encoding='utf-8', mode='r') as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter=';')
        return [row for row in reader]


def create_format(row):
    return f"{row['user_name']} | {row['date']} | {row['text']}"


def filter_msgs_by_user_id(history, user_id, counter):
    msgs = []
    for row in history:
        if row.get('user_id') == user_id:
            counter -= 1
            msgs.append(create_format(row))
        if counter <= 0:
            break
    return msgs


def date_range_format(args):
    start = "1999-01-01 00:00:00"
    end = "2999-01-01 00:00:00"

    if args:
        date_all = args.split(' ')
        start = ' '.join(date_all[:2])
        end = ' '.join(date_all[2:])

    start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    return start, end
