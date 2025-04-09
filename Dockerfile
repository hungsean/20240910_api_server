# 使用 Python 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴套件
COPY requirements.txt /app/
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 複製程式碼
COPY src /app/src
COPY assets /app/assets

# 將資產目錄加到環境變數中，讓程式可以訪問
ENV ASSETS_PATH=/app/assets

# 開啟 Port
EXPOSE 8000

# 執行 Python 應用程式
CMD ["bash", "-c", ". venv/bin/activate && python src/__main__.py"]
