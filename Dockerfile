FROM 968557029040.dkr.ecr.ap-southeast-1.amazonaws.com/esollabs/cicd:sh-python-ba4ec63-dirty


COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install "Flask[async]"

COPY . /webapps
WORKDIR /webapps