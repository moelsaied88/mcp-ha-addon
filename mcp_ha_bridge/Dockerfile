FROM python:3.11-slim

WORKDIR /app

# Install jq to read /data/options.json
RUN apt-get update && \
    apt-get install -y jq && \
    rm -rf /var/lib/apt/lists/*

COPY mcp_server.py /app/mcp_server.py
COPY run.sh /app/run.sh

RUN pip install websockets flask requests

RUN chmod +x /app/run.sh

EXPOSE 8001

CMD ["/app/run.sh"]
