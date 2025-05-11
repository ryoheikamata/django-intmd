FROM --platform=linux/arm64 python:3.12

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
	apt-get install -y gettext && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /django_intmd
EXPOSE 8000 8001

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements_dev.txt /tmp/requirements_dev.txt
COPY ./django_intmd/scripts/deployments /etc/scripts/deployments
RUN chmod +x /etc/scripts/deployments/*.sh  # 実行権限を追加
COPY . .

ARG DEV=false

RUN pip install --upgrade pip && \
	pip install -r /tmp/requirements.txt && \
	if [ $DEV = "true" ]; \
		then pip install -r /tmp/requirements_dev.txt ; \
	fi && \
	rm -rf /tmp/requirements*.txt && \
	adduser \
		--disabled-password \
		--no-create-home \
		app-user

USER app-user