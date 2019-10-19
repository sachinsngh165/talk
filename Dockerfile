FROM python:2
RUN pip install virtualenv
ADD . .
RUN virtualenv venv 
RUN /venv/bin/pip install -r requirments.txt
CMD ["/venv/bin/python", "server.py"]