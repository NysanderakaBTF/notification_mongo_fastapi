FROM python:3.11

WORKDIR /var/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./

RUN pip install --upgrade pip

COPY requirements.txt /var/www

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]