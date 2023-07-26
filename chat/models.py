from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    

class Data(models.Model):
    data_list = models.JSONField()  

    def __str__(self):
        return str(self.data_list)

my_data = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke."},
    {"role": "assistant", "content": "Why don't scientists trust atoms? Because they make up everything!"},
    {"role": "user", "content": "What's the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "Who lives in Bishkek"},
    {"role": "assistant", "content": "In Bishkek lives my bro, his name is Aibek"},
    {"role": "user", "content": "What is my name?"},
    {"role": "assistant", "content": "Your name is Thomas Shelby but your friends call you Anton"},
]

serialized_data = json.dumps(my_data)

my_model_instance = Data(data_list=my_data)
my_model_instance.save()