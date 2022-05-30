FROM python:3.9

RUN pip3.9 install Flask

COPY . /mock

WORKDIR /mock

CMD ["python3.9", "vk_id_mock.py"]