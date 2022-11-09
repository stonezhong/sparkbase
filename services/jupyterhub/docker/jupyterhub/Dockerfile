FROM jupyterhub/jupyterhub:2.3.0

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY jupyterhub_config.py ./
COPY bootstrap.py ./

# ENTRYPOINT []
# CMD ["/bin/sleep", "36000"]

CMD ["python3", "-u", "bootstrap.py"]
