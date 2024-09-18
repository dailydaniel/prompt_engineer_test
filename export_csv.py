import sqlite3
import pandas as pd


def export(save=True):

    conn = sqlite3.connect('solutions.db')

    df = pd.read_sql_query("SELECT * FROM solutions", conn)

    conn.close()

    if save:
        df.to_csv('solutions.csv', index=False)
    else:
        return df

if __name__ == "__main__":
    export()
