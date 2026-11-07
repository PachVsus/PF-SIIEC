FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home app
COPY --chown=app:app . .
RUN mkdir -p instance && chown app:app instance
ARG APP_VERSION=local
ENV APP_VERSION=$APP_VERSION
USER app
EXPOSE 8000
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "--call", "inventory:create_app"]
