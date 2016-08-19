FROM python:3-onbuild
RUN mkdir output
CMD [ "python", "./zoopla_pull.py" ]
