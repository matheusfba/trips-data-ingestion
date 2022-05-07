import sys
import logging
import pandas as pd
from sqlalchemy import create_engine


def read_file(path, columns_sort):
    try: 
        return pd.read_csv(path).sort_values(columns_sort)        
    except IOError as e:
        logging.info(f'Failed to read the file {path}.\n{str(e)}')


def save_dataframe(df, table, mode):
    engine = create_engine('postgresql://postgres:1234@localhost:5432/challenge')
    df.to_sql(table, engine, if_exists=mode)


def ingest_file(file_name):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    logging.info(f'Reading file {file_name}')
    df = read_file(file_name, ['origin_coord', 'destination_coord', 'datetime'])
    if df is None:
        logging.info('erro doido')
        return
    logging.info('Saving dataframe to trips table in PostreSQL')
    save_dataframe(df, 'trips', 'replace')