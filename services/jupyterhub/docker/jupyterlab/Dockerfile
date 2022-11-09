FROM jupyterhub/singleuser:2.3.0

USER root
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y libkrb5-dev build-essential && rm -rf /var/lib/apt/lists/*

USER jovyan
COPY --chown=1000:100 requirements.txt ./
RUN pip install pip setuptools --upgrade
RUN pip install wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=1000:100 init-spark-magic.sh ./
RUN chmod +x ./init-spark-magic.sh
RUN ./init-spark-magic.sh

COPY --chown=1000:100 spark_magic_config.json /home/jovyan/.sparkmagic/config.json

# hack, fix a sparkmagic bug for importing pandas error
COPY --chown=1000:100 sparkmagic-fixes/graphbase.py /opt/conda/lib/python3.9/site-packages/autovizwidget/plotlygraphs/graphbase.py
COPY --chown=1000:100 sparkmagic-fixes/piegraph.py  /opt/conda/lib/python3.9/site-packages/autovizwidget/plotlygraphs/piegraph.py

# ENTRYPOINT []
# CMD ["/bin/sleep", "36000"]