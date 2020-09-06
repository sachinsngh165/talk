FROM python:2
RUN pip install virtualenv
RUN virtualenv venv 
COPY server.py server.py
COPY requirments.txt requirments.txt
RUN /venv/bin/pip install -r requirments.txt
ENTRYPOINT ["/venv/bin/python", "server.py"]