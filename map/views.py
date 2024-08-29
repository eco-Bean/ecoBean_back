from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import location


# Create your views here.
@api_view(['GET'])
def get_location(request):
    location_data = location.objects.all()
    locations = []
    for i in location_data:
        data = {
            "latitude": i.latitude,
            "longitude": i.longitude,
            "name": i.name,
            "description": i.description,
            "address": i.address,
            "category": i.category,
        }
        locations.append(data)
    # chat_data = chatting.objects.filter(user=1).values()
    # history = []
    # for i in chat_data:
    #     data = {
    #         "chattingId": i["id"],
    #         "chattingQuestion": i["question"],
    #         "chattingAnswer": i["answer"],
    #         "chattingCreateAt": i["create_at"]
    #     }
    #     history.append(data)
    return Response({
        "responseDto": {
            "location": locations
        },
        "success": True,
        "error": None
    })