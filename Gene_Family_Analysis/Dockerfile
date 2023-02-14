FROM python:3.10
COPY GFA_package group4/Gene_Family_Analysis/
WORKDIR group4/Gene_Family_Analysis
ENV FLASK_APP = run.py
ENV FLASK_PORT = 5000
EXPOSE $FLASK_PORT
ENTRYPOINT ["python", "/frontend/run.py"]