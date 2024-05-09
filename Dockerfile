FROM python

WORKDIR /bot
COPY . .

RUN python -m venv venv
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["./main.py"]
