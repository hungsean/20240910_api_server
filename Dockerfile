# 使用官方的 Python 3.12 slim 版作為基礎映像
FROM python:3.12-slim-bookworm AS base

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統套件
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 從官方的 uv 映像複製 uv 執行檔
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 複製專案的 pyproject.toml 和 uv.lock 檔案
COPY pyproject.toml uv.lock /app/

# 使用 uv 安裝專案依賴，並啟用位元組碼編譯以提升效能
RUN uv sync --frozen --compile-bytecode

# 複製專案的其餘程式碼和資源
COPY . /app/

# 設定環境變數，指向 FastAPI 應用程式的主模組
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ASSETS_PATH=/app/assets

# CMD ["python", "src/__main__.py"]
