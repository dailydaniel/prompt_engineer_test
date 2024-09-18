import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import json

load_dotenv()

from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url=os.environ['LLM_HOST']
)

model = os.environ['MODEL']

with open('tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

conn = sqlite3.connect('solutions.db', check_same_thread=False)
cursor = conn.cursor()

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
        st.markdown(tasks['task1'])

        temperature1 = st.number_input("Укажите температуру для Задачи 1", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

        prompt1 = st.text_area("Введите ваш промпт для Задачи 1")

        submitted1 = st.form_submit_button("Сгенерировать ответ для Задачи 1")

        if submitted1:
            if prompt1:
                st.session_state['temperature1'] = temperature1
                st.session_state['prompt1'] = prompt1

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
        st.markdown(tasks['task2'])

        temperature2 = st.number_input("Укажите температуру для Задачи 2", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

        prompt2 = st.text_area("Введите ваш промпт для Задачи 2")

        submitted2 = st.form_submit_button("Сгенерировать ответ для Задачи 2")

        if submitted2:
            if prompt2:
                st.session_state['temperature2'] = temperature2
                st.session_state['prompt2'] = prompt2

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

            for key in required_keys:
                st.session_state.pop(key, None)
        else:
            st.warning("Пожалуйста, заполните все поля перед отправкой.")

conn.close()
