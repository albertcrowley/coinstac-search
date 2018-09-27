FROM coinstac/coinstac-base-python-stream

VOLUME ["/mnt/data"]

# Set the working directory to /app
WORKDIR /computation


RUN apt-get update
RUN apt-get -y install graphviz
RUN git clone https://github.com/incf-nidash/PyNIDM.git

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN sh /computation/Miniconda3-latest-Linux-x86_64.sh -p /home/node/miniconda3 -f -b
RUN echo 'export PATH=/home/node/miniconda3/bin:$PATH' >> ~/.bashrc


RUN    echo 'export PATH=/home/node/miniconda3/bin:$PATH' >> /home/node/.bashrc
ENV PATH="/home/node/miniconda3/bin:$PATH"
RUN echo $PATH
RUN conda create -n pynidm_py3 python=3 pytest graphviz -y
RUN chmod +x /home/node/miniconda3/bin/activate
RUN activate pynidm_py3
RUN cd /computation/PyNIDM && pip install -e .
RUN cd /computation/PyNIDM && pip install rdflib requests fuzzywuzzy owlready2 pygithub pybids duecredit

# Copy the current directory contents into the container at /app
ADD . /computation


# Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

