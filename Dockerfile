FROM thomasweise/texlive
RUN apt-get update -y
RUN apt-get install python3 python3-pip -y
ADD *.py /doc/
ADD *.tex /doc/
ADD requirements.txt /
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]
