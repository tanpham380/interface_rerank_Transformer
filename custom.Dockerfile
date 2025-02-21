FROM custom-local-reranker

WORKDIR /app
RUN rm -rf /app/models/*


COPY ./local-ranker-model/ /app/models/model/

# RUN python3 download.py 
ENTRYPOINT ["./entrypoint.sh"]