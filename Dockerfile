FROM python:2.7
COPY ./python/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p /out
COPY ./python /app
#CMD ["python", "app.py"]
