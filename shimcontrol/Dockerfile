FROM python:3-slim

ARG shimcontrol_user_id=1000

RUN useradd --system --uid $shimcontrol_user_id shimcontrol

RUN mkdir /usr/share/shimcontrol

WORKDIR /usr/share/shimcontrol

COPY requirements.txt /usr/share/shimcontrol/

COPY . /usr/share/shimcontrol

USER shimcontrol

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
