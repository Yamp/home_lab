FROM edoburu/pgbouncer:latest

USER root

RUN mkdir -p /var/log/pgbouncer/ && chmod 755 /var/log/pgbouncer/ && touch /var/log/pgbouncer/pgbouncer.log && \
    chmod 544 /var/log/pgbouncer/pgbouncer.log
USER postgres
