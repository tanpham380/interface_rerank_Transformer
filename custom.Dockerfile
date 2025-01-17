FROM local-reranker

WORKDIR /app
RUN rm -rf /app/models

RUN python3 download.py 
ENTRYPOINT ["./entrypoint.sh"]