import sys
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def read_file(path, columns_sort):
    try: 
        return pd.read_csv(path).sort_values(columns_sort)        
    except IOError as e:
        print(f'Failed to read the file {path}.')
        print(e)



def save_dataframe(df, table, mode):
    engine = create_engine('postgresql://postgres:1234@localhost:5432/challenge')
    df.to_sql(table, engine, if_exists=mode)
    
    

def main(args):
    print('Getting files list')
    files = args[1].split(",")
    print(f'Files to ingest: {files}')

    for file_name in files:
        print(f'Reading file {file_name}')
        df = read_file(file_name, ['origin_coord', 'destination_coord', 'datetime'])
        if df is None:
            continue
        print('Saving dataframe to trips table in PostreSQL')
        save_dataframe(df, 'trips', 'replace')
    print('Finished!')
    
    
if __name__ == "__main__":
    main(sys.argv)