FROM postgres:11

COPY ./docker/postgres/maintenance /usr/local/bin/maintenance
COPY ./docker/postgres/postgresql.conf /data/postgres/
COPY ./docker/postgres/postgres_logrotate.conf /etc/logrotate.d/

RUN ln -s /usr/lib/postgresql/11/bin/pg_ctl /usr/bin/pg_ctl && chmod 777 /usr/bin/pg_ctl && \
    chmod +x /usr/local/bin/maintenance/* && mv /usr/local/bin/maintenance/* /usr/local/bin && \
    rmdir /usr/local/bin/maintenance
