FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY program_service.py server.py ./

ENV MCP_TRANSPORT=streamable-http
ENV PORT=8080

EXPOSE 8080

CMD ["python", "server.py"]
