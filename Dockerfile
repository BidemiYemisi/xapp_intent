FROM python:3.8-alpine

WORKDIR /app

# copy rmr files from builder image in lieu of an Alpine package
COPY --from=nexus3.o-ran-sc.org:10002/o-ran-sc/bldr-alpine3-rmr:4.0.5 /usr/local/lib64/librmr* /usr/local/lib64/

COPY --from=nexus3.o-ran-sc.org:10002/o-ran-sc/bldr-alpine3-rmr:4.0.5 /usr/local/bin/rmr* /usr/local/bin/
ENV LD_LIBRARY_PATH=/usr/local/lib/:/usr/local/lib64


# sdl needs gcc
RUN apk update && apk add gcc musl-dev bash

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY xapp_intent ./xapp_intent
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "xapp_intent.main"]
