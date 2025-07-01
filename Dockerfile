# Візьмемо офіційний легкий образ Python 3.11
FROM python:3.11-slim

# Папка в контейнері для твого коду
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код у контейнер
COPY . .

# Команда запуску бота
CMD ["python", "translate_bot.py"]
