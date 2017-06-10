FROM eywalker/tensorflow-jupyter:v0.11.0rc0

RUN pip3 install seaborn
RUN pip3 install git+https://github.com/datajoint/datajoint-python.git

ADD . /src
RUN pip3 install -e /src
