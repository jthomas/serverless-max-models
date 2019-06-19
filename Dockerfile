ARG model
FROM codait/${model}:latest

ADD openwhisk.py .

EXPOSE 8080

CMD python openwhisk.py
