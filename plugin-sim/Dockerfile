FROM coinstac/coinstac-base-python-stream

VOLUME ["/mnt/data"]

WORKDIR /opt


RUN apt-get update &&  \
    apt-get install -y git python3 graphviz python3-pip ssh mercurial python-setuptools

RUN python3 -m pip install --upgrade pip && \
    pip3 install rdflib requests fuzzywuzzy pygithub pybids duecredit setuptools \
                 python-Levenshtein pytest graphviz prov pydot validators ontquery \
                 click rdflib-jsonld pyld tabulate

RUN pip3 install Owlready2

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN update-alternatives --remove python /usr/bin/python2 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

RUN cd / && \
    git clone https://github.com/albertcrowley/PyNIDM.git && \
    mv PyNIDM PyNIDM-snapshot && \
    cd PyNIDM-snapshot && \
    pip install -e .

RUN mkdir /computation
WORKDIR /computation

# Copy the current directory contents into the container at /app
ADD . /computation



