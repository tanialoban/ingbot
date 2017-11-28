FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/btelegr/
COPY . /usr/btelegr/
WORKDIR /usr/btelegr/

EXPOSE 8349

CMD ["python3", "-u", "gbtelegr.py"]
 
