# main/views.py
import json
from django.shortcuts import get_object_or_404
from .models import Mission_User_mapping
from users.models import users
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def main_page(request, user_id):
    user = get_object_or_404(users, id=user_id)

    # Fetch daily missions related to the user
    missions = Mission_User_mapping.objects.filter(user=user)

    # Prepare the mission data for the response
    mission_data = []
    for mission_map in missions:
        mission = mission_map.mission
        mission_data.append({
            "mappingId": mission_map.id,
            "content": mission.content,
            "point": mission.point,
            "achieve": mission_map.achieve,
        })

    # Construct the response data structure
    response_data = {
        "responseDto": {
            "missionDate": missions[0].date if missions.exists() else None,
            "mission": mission_data,
        },
        "success": True,
        "error": None
    }

    return JsonResponse(response_data)

@csrf_exempt  # This is for testing purposes only; remove in production.
@require_POST
def accomplish_mission(request):
    # Extract userId from request headers
    user_id = request.headers.get('userId')

    try:
        # Parse JSON body
        data = json.loads(request.body)
        mission_mapping_id = data.get('missionMappingId')
    except json.JSONDecodeError:
        return JsonResponse({
            "responseDto": None,
            "success": False,
            "error": "Invalid JSON format."
        })

    # Validate input
    if not mission_mapping_id:
        return JsonResponse({
            "responseDto": None,
            "success": False,
            "error": "missionMappingId is required."
        })

    # Fetch the mission mapping object and update the achieve field
    mission_mapping = get_object_or_404(Mission_User_mapping, id=mission_mapping_id, user_id=user_id)
    mission_mapping.achieve = True
    mission_mapping.save()

    # Construct response data
    response_data = {
        "responseDto": {
            "missionId": mission_mapping.mission.id,
        },
        "success": True,
        "error": None
    }

    return JsonResponse(response_data)