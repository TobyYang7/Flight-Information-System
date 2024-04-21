import mysql.connector
import numpy as np
import pandas as pd
import json
from time import time
from typing import List, Dict

EPS = 1e-10


def prepare_cursor():
    with open('fis_config.json') as f:
        config = json.load(f)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    return cursor, cnx


def insert_csv_to_database(path: str, table_name: str, column_map: Dict[str, str], batch_size=10000):
    _t0 = time()
    df_chunks = pd.read_csv(path, chunksize=batch_size)
    # import pdb; pdb.set_trace()
    db_columns, csv_columns = list(zip(*column_map.items()))

    statement = f"""
        insert ignore into {table_name} ({', '.join(db_columns)})
        values
    """

    # df = df.replace({np.nan: None})
    # records = df.to_records(index=False).tolist()

    cursor, cnx = prepare_cursor()
    cursor.execute('SET autocommit=0;')

    record_cnt = 0
    print('start insertion.')
    for i, df in enumerate(df_chunks):
        # print(df)
        t0 = time()
        df = df[list(csv_columns)]
        items = df.replace({np.nan: None}).to_records(index=False).tolist()
        items_str = [f"({', '.join(map(lambda x: repr(x) if x is not None else 'NULL', item))})"
                     for item in items]
        insert_stmt = statement + f"{', '.join(items_str)};"
        cursor.execute(insert_stmt)
        record_cnt += cursor.rowcount
        print(f'inserted [{(i+1)*batch_size:6d}], {cursor.rowcount} new rows, avg {batch_size/(time()-t0 + EPS):.2f} records/s')

    cnx.commit()

    print(f'{record_cnt} was inserted to {table_name} in {time()-_t0:.2f}s')


def load_data_config(path: str):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


if __name__ == "__main__":
    data_config = load_data_config('data_config.json')
    for table, col_map in data_config.items():
        print(f'inserting data for {table}')
        insert_csv_to_database(f'data/{table}.csv', table, col_map, 10000)
