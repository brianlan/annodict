FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN mkdir -p /code/webapp
COPY ./requirements.txt /code/webapp
RUN pip install -r /code/webapp/requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple

COPY . /code/webapp
WORKDIR /code/webapp

# CMD tail -f /dev/null

CMD ["gunicorn", "--bind", "0.0.0.0:5100", "app:app"]
# CMD python app.py