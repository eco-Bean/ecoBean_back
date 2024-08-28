# mypage/views.py
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User_Challenge_mapping, Challenge
from users.models import users
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from chatting.utils import s3_file_upload_by_file_data

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

@csrf_exempt
@require_POST
def upload_challenge_image(request):
    try:
        # Extract userId from request headers
        user_id = request.headers.get('userId')

        if not user_id:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "userId is required."
            })

        # Fetch the user object
        user = get_object_or_404(users, id=user_id)

        # Validate if an image is provided
        if 'image' not in request.FILES:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "No image provided."
            })

        # Validate if a challenge_id is provided
        challenge_id = request.POST.get('challenge_id')
        if not challenge_id:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "challenge_id is required."
            })

        # Fetch the challenge object
        challenge = get_object_or_404(Challenge, id=challenge_id)

        # Upload the file to S3 and get the URL
        image = request.FILES['image']
        image_url = s3_file_upload_by_file_data(upload_file=image)

        if not image_url:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "Failed to upload image to S3."
            })

        # Save the challenge mapping with the image URL
        user_challenge_mapping = User_Challenge_mapping.objects.create(
            user=user,
            challenge=challenge,
            image=image_url,  # Save the S3 URL in the database
            achieve_at=now()
        )

        # Construct the response data
        response_data = {
            "responseDto": {
                "challengeId": user_challenge_mapping.challenge.id,
                "imageUrl": user_challenge_mapping.image  # This is now the URL string
            },
            "success": True,
            "error": None
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({
            "responseDto": None,
            "success": False,
            "error": str(e)
        }, status=500)
