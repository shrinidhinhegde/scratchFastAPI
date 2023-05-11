FROM python:3.9

LABEL author="Shrinidhi Hegde"

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:src/"

EXPOSE 8000

CMD ["python3", "src/main.py"]