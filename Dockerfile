FROM python


RUN python -m pip install Flask psutil  prometheus_client

ADD app.py /

CMD ["python","/app.py"]