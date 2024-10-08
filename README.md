# prompt_engineer_test
repo for test tasks for prompt engineer

# Инструкция по запуску приложения

Данное приложение разработано на `Streamlit` и использует библиотеку `openai` для взаимодействия с языковой моделью. Приложение хранит данные в базе данных `SQLite`.

## Требования

- Python 3.7 или выше
- Ключ API OpenAI / OpenAI like

## Шаги по установке и запуску

### Docker

### 1. Клонируйте репозиторий или скачайте исходный код

### 2. Создайте и активируйте виртуальное окружение

### 3. Запустите проект

```bash
docker build -t pen-test-streamlit .
docker run -d -p 8501:8501 -p 8503:8503 pen-test-streamlit
```

### Локальная установка

### 1. Клонируйте репозиторий или скачайте исходный код

### 2. Создайте и активируйте виртуальное окружение

#### Для Windows:

Откройте командную строку и выполните следующие команды:

```bash
python -m venv venv
source venv/bin/activate
```

#### Для macOS/Linux:

Откройте терминал и выполните следующие команды:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости

Убедитесь, что вы находитесь в активированном виртуальном окружении. Установите необходимые библиотеки из файла `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения в .env

### 5. При необходимости измените задания в tasks.json

### 6. Запустите приложение

В командной строке или терминале выполните команду:

```bash
streamlit run main.py
streamlit run admin_app.py
```

### 7. Использование приложения

- Откроется веб-интерфейс приложения в вашем браузере.
- Введите ваше ФИО.
- Прочитайте описание тестового задания и выполните обе задачи, введя свои промпты.
- Нажмите кнопки "Сгенерировать ответ" для каждой задачи, чтобы получить ответы модели.
- После того как обе задачи будут выполнены, нажмите кнопку "Отправить решение" для сохранения результатов в базу данных.
