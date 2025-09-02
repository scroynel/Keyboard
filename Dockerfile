# FROM python:3.12.11-bookworm

# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# RUN apt-get update && apt-get install -y curl
# RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
#     apt-get install -y nodejs

# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# COPY ./requirements.txt .

# RUN uv pip install pip --upgrade --system
# RUN uv pip install -r requirements.txt --system

# RUN cd theme/static_src && npm install

# RUN npm install -D tailwindcss
# RUN npm --prefix theme/static_src run build:tailwind

# COPY . .

# EXPOSE 8000

# CMD ["sh", "entrypoint.sh"]

FROM python:3.12.11-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy requirements and install Python deps early
COPY ./requirements.txt .
RUN uv pip install pip --upgrade --system
RUN uv pip install -r requirements.txt --system

# Copy the rest of the app early
COPY . .

# Install frontend dependencies and build assets
RUN cd theme/static_src && npm install
RUN npm install -D tailwindcss
RUN npm --prefix theme/static_src run build:tailwind

# Ensure entrypoint is executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]