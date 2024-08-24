from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import questionSerializer, chattingSerializer, recycleSerializer
from .utils import gemini_answer, get_history, s3_file_upload_by_file_data, gemini_img, recycle_img
from users.models import users
from .models import chatting

# Create your views here.

@api_view(['POST'])
def chat(request):
    serializer = questionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.data['chattingQuestion']
        history = get_history(1)
        image = request.data['chattingImage']
        if image != "":
            file = s3_file_upload_by_file_data(image)
            answer = gemini_img(question, file, history)
        else:
            file = ""
            answer = gemini_answer(question, history)
        data = {
            "question": question,
            "answer": answer,
            "file": file,
            "user": 1,
        }
        chatting_serializer = chattingSerializer(data=data)
        chatting_serializer.is_valid(raise_exception=True)
        chatting_serializer.save()
        return Response({
            "responseDto": {
                "chattingAnswer": answer,
            },
            "success": True,
            "error": None
        })

@api_view(['GET'])
def chat_history(request):
    chat_data = chatting.objects.filter(user=1).values()
    history = []
    for i in chat_data:
        data = {
            "chattingId": i["id"],
            "chattingQuestion": i["question"],
            "chattingAnswer": i["answer"],
            "chattingCreateAt": i["create_at"]
        }
        history.append(data)
    return Response({
        "responseDto": {
            "history": history
        },
        "success": True,
        "error": None
    })

@api_view(['POST'])
def recycle(request):
    image = request.data['recycleImage']
    file = s3_file_upload_by_file_data(image)
    answer = recycle_img(file)
    return Response({
        "responseDto": {
            "recycleAnswer": answer,
        },
        "success": True,
        "error": None
    })