from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import openai
from .models import Data
from django.core import serializers
import json
# openai.api_key = config('OPENAI_KEY') # 1st key

def ask_openai(my_data, message):
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": my_data},
        {"role": "user", "content": message},
    ]
    )

    answer = response.choices[0]['message']['content']
    return answer

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        # with open('/Users/aibekworllld/Desktop/ev.28/job/chatclone/data/info.txt', 'r', encoding='utf-8') as file:
        #     my_data = file.read()
        queryset = Data.objects.all()
        my_data = []
        for obj in queryset:
            my_data.extend(obj.data_list)
        message = request.data.get('message')
        if message is None:
            return Response({'detail': 'Field "message" is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data_json = json.dumps(my_data)
            response = ask_openai(data_json, message)
            return Response({'message': message, 'response': response})
        except Exception as e:
            return Response({'detail': 'Error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, format=None):
        return Response({'detail': 'GET method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, format=None):
        return Response({'detail': 'PUT method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, format=None):
        return Response({'detail': 'DELETE method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

