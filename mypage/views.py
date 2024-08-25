# mypage/views.py

from django.http import JsonResponse
from users.models import users
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

@require_GET
def user_profile_detail(request):
    # Extract userId from request headers
    user_id = request.headers.get('userId')

    # Validate input
    if not user_id:
        return JsonResponse({
            "responseDto": None,
            "success": False,
            "error": "userId is required."
        })

    # Fetch the user object
    user = get_object_or_404(users, id=user_id)

    # Construct the response data
    response_data = {
        "responseDto": {
            "userNickname": user.nickname,
            "userProfileImage": user.profile_image,
            "userPoint": user.point
        },
        "success": True,
        "error": None
    }

    return JsonResponse(response_data)
