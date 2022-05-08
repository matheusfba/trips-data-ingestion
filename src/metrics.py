import sys
import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')


def show_report(file):
    sql_file = open(f'/app/sql/{file}','r')
    df = pd.read_sql(sql_file.read(), engine)    
    print(tabulate(df, headers='keys', tablefmt='psql'))

    
def main(args):
    print('======================================================================================')
    print('Weekly average number of trips for an area:')
    show_report('weekly_avg_trips.sql')
    print('======================================================================================')
    print('From the two most commonly appearing regions, which is the latest datasource?')
    show_report('latest_datasource.sql')
    print('======================================================================================')
    print('What regions has the "cheap_mobile" datasource appeared in?')
    show_report('cheap_mobile_appearance.sql')
    print('======================================================================================')
    print('END')

if __name__ == "__main__":    
    main(sys.argv)