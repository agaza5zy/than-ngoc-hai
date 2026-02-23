# Sử dụng Python 3.10
FROM python:3.10-slim

# Biến môi trường: 1=Không tạo file .pyc, 1=Log hiện ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thư mục làm việc trong container
WORKDIR /app

# Cài đặt thư viện
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . /app/

# Mở port 8000
EXPOSE 8000

# Lệnh chạy mặc định
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
