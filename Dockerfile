FROM python:3.8
COPY . /code
RUN pip install -r /code/requirements.txt
EXPOSE 5000
CMD  ["python","-u","/code/app.py"]
