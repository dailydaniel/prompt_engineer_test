import sqlite3
import pandas as pd

# Подключение к базе данных
conn = sqlite3.connect('solutions.db')

# Чтение данных в DataFrame
df = pd.read_sql_query("SELECT * FROM solutions", conn)

# Сохранение в CSV
df.to_csv('solutions.csv', index=False)

# Закрытие соединения
conn.close()
