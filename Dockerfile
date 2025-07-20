FROM python:3.10.18-slim

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . .

ENV PINECONE_API_KEY=""
ENV GROQ_API_KEY=""

EXPOSE 8000

CMD ["chainlit", "run", "app_cl.py", "--host", "0.0.0.0"]