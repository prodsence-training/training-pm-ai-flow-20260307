# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製原始碼
COPY . .

# 暴露端口
EXPOSE 8000

# 啟動應用程式
CMD ["python", "-m", "src.main"]
