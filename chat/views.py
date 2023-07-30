from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import openai
from .models import Data
from django.core import serializers
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('wordnet')
# openai.api_key = config('OPENAI_KEY') # 1st key

def preprocess_text(text):
    sentences =sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    processed_data = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
        processed_data.append(" ".join(lemmatized_words))

    processed_data_text = "\n".join(processed_data)
    return processed_data_text

def ask_openai(my_data, message):
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": my_data},
        {"role": "user", "content": message},
    ]
    )

    answer = response.choices[0]['message']['content']

    user_message = {"role": "user", "content": message}
    bot_message = {"role": "assistant", "content": answer}

    try:
        with open('/Users/aibekworllld/Desktop/ev.28/job/chatclone/data/info.json', 'r', encoding='utf-8') as chat_file:
            chat_data = json.load(chat_file)
    except FileNotFoundError:
        chat_data = []

    chat_data.append(user_message)
    chat_data.append(bot_message)

    with open('/Users/aibekworllld/Desktop/ev.28/job/chatclone/data/info.json', 'w', encoding='utf-8') as chat_file:
        json.dump(chat_data, chat_file)

    # answer = response.choices[0]['message']['content']
    return answer



class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        if request.content_type != 'application/json':
            return Response({'detail': 'Invalid content type. Expected JSON.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message_data = json.loads(request.body)
            message = message_data.get('message')
        except json.JSONDecodeError:
            return Response({'detail': 'Invalid JSON data.'}, status=status.HTTP_400_BAD_REQUEST)

        # For reading data from fail
        with open('/Users/aibekworllld/Desktop/ev.28/job/chatclone/data/info.json', 'r', encoding='utf-8') as file:
            my_data = file.read()
            processed_data = preprocess_text(my_data)

        try:
            response = ask_openai(processed_data, message)
            return Response({'message': message, 'response': response})
        except Exception as e:
            return Response({'detail': 'Error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # For reading data in database
        # queryset = Data.objects.all()
        # my_data = []
        # for obj in queryset:
        #     my_data.extend(obj.data_list)
            
        # message = request.data.get('message')
        
        
        # if message is None:
        #     return Response({'detail': 'Field "message" is required'}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     data_json = json.dumps(my_data)
        #     response = ask_openai(data_json, message)

            # my_data.append({"role": "user", "content": message})
            # my_data.append({"role": "assistant", "content": response})
            # data_instance = Data.objects.create(data_list=my_data)
            
        #     return Response({'message': message, 'response': response})
        # except Exception as e:
        #     return Response({'detail': 'Error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, format=None):
        return Response({'detail': 'GET method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, format=None):
        return Response({'detail': 'PUT method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, format=None):
        return Response({'detail': 'DELETE method not allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

