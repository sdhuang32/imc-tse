FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY imports.py ./
ENV PYTHONSTARTUP ./imports.py

COPY . .

# Unit test section
#
# In case temporary files or testing data are going to be generated,
# we should use a multi-stage build and exclude those files to save
# the final image space
RUN python -m torture

CMD [ "python" ]
