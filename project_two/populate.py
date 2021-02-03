#!/usr/bin/env python
from faker import Faker
from app.models import User
import random
import django
import os


django.setup()
fake = Faker()


def populate(N: 5):
    for entry in range(N):
        username = fake.name().split()
        first_name = username[0]
        last_name = username[1]
        email_fake = fake.email()
        User.objects.get_or_create(
            firstName=first_name, lastName=last_name, email=email_fake)


if __name__ == '__main__':
    print("populate date")
    populate(20)
    print('finished')
