FROM python:3.7.7-slim-stretch
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY app.py app.py
CMD ["streamlit","run","app.py"]