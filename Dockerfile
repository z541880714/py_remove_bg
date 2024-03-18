FROM  python:3.9
LABEL authors="lionel"

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD["python", "clean_bg.py"]