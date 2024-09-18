FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка Supervisor
RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /app/logs

COPY . .

# Открываем порты для приложений
EXPOSE 8501
EXPOSE 8503

# Копируем конфигурацию Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Запуск Supervisor
CMD ["/usr/bin/supervisord"]
