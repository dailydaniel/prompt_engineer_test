import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import json

# Загрузка переменных окружения из .env файла
load_dotenv()

# Инициализация клиента OpenAI-like
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url=os.environ['LLM_HOST']
)

model = os.environ['MODEL']

# Загрузка описаний задач из файла tasks.json
with open('tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# Установка соединения с базой данных SQLite
conn = sqlite3.connect('solutions.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS solutions (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    prompt1 TEXT,
    output1 TEXT,
    temperature1 REAL,
    prompt2 TEXT,
    output2 TEXT,
    temperature2 REAL
)
''')
conn.commit()

st.set_page_config(
    page_title="prompt engineer test",
    page_icon="🤖",
    layout="wide",
)

st.title("Тестовое задание для промпт инженера")

# Поле для ввода ФИО
full_name = st.text_input("Введите ваше ФИО")

if full_name:
    st.write(f"Здравствуйте, {full_name}!")

    st.header("Описание тестового задания")

    st.markdown(f"""
    **Задача 1:**
    {tasks['task1']}

    **Задача 2:**
    {tasks['task2']}
    """)

    st.subheader("Задача 1")

    with st.form("form1"):
        # Отображение описания задачи
        st.markdown(tasks['task1'])

        # Выбор температуры
        # temperature1 = st.number_input("Укажите температуру для Задачи 1", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="temperature1")
        temperature1 = st.number_input("Укажите температуру для Задачи 1", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

        # Ввод промпта
        # prompt1 = st.text_area("Введите ваш промпт для Задачи 1", value=st.session_state.get('prompt1', ''))
        prompt1 = st.text_area("Введите ваш промпт для Задачи 1")

        submitted1 = st.form_submit_button("Сгенерировать ответ для Задачи 1")

        if submitted1:
            if prompt1:
                # Сохранение выбора в сессии
                st.session_state['temperature1'] = temperature1
                st.session_state['prompt1'] = prompt1

                # Функция для генерации ответа
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt1}],
                        max_tokens=2048,
                        temperature=temperature1
                    )

                    output1 = response.choices[0].message.content.strip()
                    st.session_state['output1'] = output1
                    st.write("Ответ модели для Задачи 1:")
                    st.write(output1)
                except Exception as e:
                    st.error(f"Произошла ошибка при генерации ответа: {e}")
            else:
                st.warning("Пожалуйста, введите промпт для Задачи 1.")
        elif 'output1' in st.session_state:
            st.write("Ответ модели для Задачи 1:")
            st.write(st.session_state['output1'])

    st.subheader("Задача 2")

    with st.form("form2"):
        # Отображение описания задачи
        st.markdown(tasks['task2'])

        # Выбор температуры
        # temperature2 = st.number_input("Укажите температуру для Задачи 2", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="temperature2")
        temperature2 = st.number_input("Укажите температуру для Задачи 2", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

        # Ввод промпта
        # prompt2 = st.text_area("Введите ваш промпт для Задачи 2", value=st.session_state.get('prompt2', ''))
        prompt2 = st.text_area("Введите ваш промпт для Задачи 2")

        submitted2 = st.form_submit_button("Сгенерировать ответ для Задачи 2")

        if submitted2:
            if prompt2:
                # Сохранение выбора в сессии
                st.session_state['temperature2'] = temperature2
                st.session_state['prompt2'] = prompt2

                # Функция для генерации ответа
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt2}],
                        max_tokens=2048,
                        temperature=temperature2
                    )

                    output2 = response.choices[0].message.content.strip()
                    st.session_state['output2'] = output2
                    st.write("Ответ модели для Задачи 2:")
                    st.write(output2)
                except Exception as e:
                    st.error(f"Произошла ошибка при генерации ответа: {e}")
            else:
                st.warning("Пожалуйста, введите промпт для Задачи 2.")
        elif 'output2' in st.session_state:
            st.write("Ответ модели для Задачи 2:")
            st.write(st.session_state['output2'])

    # Кнопка для отправки решения
    if st.button("Отправить решение"):
        required_keys = ['prompt1', 'output1', 'temperature1', 'prompt2', 'output2', 'temperature2']
        if full_name and all(key in st.session_state for key in required_keys):
            cursor.execute('''
                INSERT INTO solutions (full_name, prompt1, output1, temperature1, prompt2, output2, temperature2)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                full_name,
                st.session_state['prompt1'],
                st.session_state['output1'],
                st.session_state['temperature1'],
                st.session_state['prompt2'],
                st.session_state['output2'],
                st.session_state['temperature2']
            ))
            conn.commit()
            st.success("Ваше решение было отправлено!")
            # Очистка сессии
            for key in required_keys:
                st.session_state.pop(key, None)
        else:
            st.warning("Пожалуйста, заполните все поля перед отправкой.")

# Закрытие соединения с базой данных
conn.close()
