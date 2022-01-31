FROM python:alpine
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
CMD python ./weather-app.py 