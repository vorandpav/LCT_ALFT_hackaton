FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY . .

RUN mkdir -p /app/photos

EXPOSE 9000

CMD ["uvicorn", "fake_camera.main:app", "--host", "0.0.0.0", "--port", "9000"]
