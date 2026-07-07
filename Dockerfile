FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY config ./config
COPY examples ./examples
COPY src ./src
COPY tests ./tests

RUN pip install --no-cache-dir -e ".[dev]"

CMD ["python", "-m", "agentguard.main", "assess", "--case", "financial_advisor_copilot"]
