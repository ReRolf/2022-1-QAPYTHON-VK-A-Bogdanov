from faker import Faker

fake = Faker()


def create_name():
    return fake.first_name()


def create_job():
    return f'{fake.job()}'
