FROM python:2.7
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p /out
COPY . /app
#CMD ["python", "app.py"]
