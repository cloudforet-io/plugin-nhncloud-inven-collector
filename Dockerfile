FROM cloudforet/python-core:2.0

ENV PYTHONUNBUFFERED 1
ENV SPACEONE_PORT 50051
ENV SRC_DIR /tmp/src
ENV CONF_DIR /opt/spaceone

COPY . ${SRC_DIR}
WORKDIR ${SRC_DIR}
RUN pip install .
RUN rm -rf ${SRC_DIR}

RUN mkdir -p ${CONF_DIR}
WORKDIR ${CONF_DIR}

EXPOSE ${SPACEONE_PORT}

ENTRYPOINT ["spaceone"]
CMD ["run", "plugin-server", "plugin"]
