# ==============================
# 1️⃣ Base Image
# ==============================
FROM python:3.11-slim

# ==============================
# 2️⃣ Environment setup
# ==============================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ==============================
# 3️⃣ Set working directory
# ==============================
WORKDIR /app

# ==============================
# 4️⃣ Install dependencies
# ==============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise python-dotenv

# ==============================
# 5️⃣ Copy project files into container
# ==============================
COPY . .

# ==============================
# 6️⃣ Run migrations + collect static files
# ==============================
RUN python manage.py makemigrations main --noinput
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# ==============================
# 7️⃣ Expose port
# ==============================
EXPOSE 8000

# ==============================
# 8️⃣ Start Gunicorn server
# ==============================
CMD ["gunicorn", "jotravels.wsgi:application", "--bind", "0.0.0.0:8000"]
