FROM python:alpine3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 4000
ENTRYPOINT ["python"]
CMD ["adtgenerator.py"]
