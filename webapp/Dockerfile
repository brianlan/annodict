FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN mkdir -p /code/webapp
COPY ./requirements.txt /code/webapp
RUN pip install -r /code/webapp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /code/webapp
WORKDIR /code/webapp
CMD python app.py
#CMD tail -f /dev/null