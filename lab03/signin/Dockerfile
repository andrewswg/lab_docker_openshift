FROM python
COPY ./Requirements.txt /Requirements.txt
WORKDIR /
RUN pip install -r Requirements.txt
COPY . /
ENTRYPOINT [ "python3" ]
CMD [ "signin.py" ]