from .models import Expense,User 
from django.db.models.signals import post_save
from django.dispatch import receiver
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
@receiver(post_save, sender=User)
def create_expense(sender,instance,created,**kwargs): 
  if created:
    user_id = instance.id 
    mydb = myclient["learn_api"]
    mycol = mydb["api_app_expense"]
    data = {
      "id":user_id,
      "category":"",
      "amunt":0 , 
      "price":0,
      "array":[],
      "embedded":{} , 
      "imgs":[]
    }
    return_data= mycol.insert_one(data)
    