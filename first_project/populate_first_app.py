#!/usr/bin/env python
from first_app.models import Topic, AccessRecord, Webpage
from faker import Faker
import random
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

fake = Faker()
topics = ["topic1", "topic2", "tpic3", "topic4"]
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t


def populate(N=5):
    for entry in range(N):

        topic_entry = add_topic()
        fake_url = fake.url()
        fake_date = fake.date()
        fake_name = fake.company()
        weppg = Webpage.objects.get_or_create(
            Topic=topic_entry, name=fake_name, url=fake_url)[0]
        acc_rec = AccessRecord.objects.get_or_create(
            name=weppg, date=fake_date)


if __name__ == "__main__":
    print("papulate script")
    populate(20)
    print("populate complete")
