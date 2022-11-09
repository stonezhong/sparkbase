FROM apache/airflow:2.3.0-python3.8

COPY --chown=50000:0 webserver_config.py ./
COPY --chown=50000:0 bootstrap.py ./

RUN mkdir /home/airflow/state
ENTRYPOINT []
# CMD ["/bin/sleep", "36000"]
CMD /usr/bin/dumb-init -- python -u bootstrap.py
