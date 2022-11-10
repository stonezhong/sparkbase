FROM apache/superset:7a2eb8b602bf1701aa5641f23577d45adef4e37d

COPY --chown=superset:superset requirements.txt ./
RUN pip install wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=superset:superset config.py ./superset
COPY --chown=superset:superset bootstrap.py ./

# We need to track if superset has been initialized or not
# We will put a file .upgrade file in it after initialization
# See bootstrap.py
RUN mkdir /app/superset_home/state

ENTRYPOINT []
# CMD ["/bin/sleep", "36000"]
CMD ["python", "-u", "bootstrap.py"]
