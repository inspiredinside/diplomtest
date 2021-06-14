FROM python:3.8-alpine
RUN apk update
WORKDIR /opt/flask-app
ENV VIRTUAL_ENV=/opt/flask-app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN python3 -m pip install --upgrade setuptools
#RUN pip3 install --no-cache-dir  --force-reinstall -Iv grpcio==1.36.1
ADD requirements.txt requirements.txt
#RUN python3 -m venv venv
RUN pip3 install -r requirements.txt
ADD  . .
EXPOSE 5000
CMD ["python3", "app.py"]
