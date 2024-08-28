# store/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from users.models import users
from .models import User_Product_mapping, Product
from django.shortcuts import get_object_or_404


def product_list(request):
    # Retrieve all products from the Product table
    products = Product.objects.all()

    # Prepare the response data
    product_list = [
        {
            "productId": product.id,
            "productName": product.name,
            "productPrice": product.price,
        }
        for product in products
    ]

    response_data = {
        "responseDto": {
            "productList": product_list,
        },
        "success": True,
        "error": None,
    }

    return JsonResponse(response_data)

def user_purchased_items(request):
    # Extract userId from request headers
    user_id = request.headers.get('userId')

    if not user_id:
        return JsonResponse({
            "responseDto": None,
            "success": False,
            "error": "userId is required."
        })

    # Retrieve all products purchased by the user
    purchased_items = User_Product_mapping.objects.filter(user_id=user_id)

    # Prepare the response data
    purchased_list = [
        {
            "productId": item.product.id,
            "productName": item.product.name,
            "productPrice": item.product.price,
        }
        for item in purchased_items
    ]

    response_data = {
        "responseDto": {
            "productList": purchased_list,
        },
        "success": True,
        "error": None,
    }

    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def purchase_item(request):
    try:
        # Extract userId and productId from request headers or body
        user_id = request.POST.get('userId')
        product_id = request.POST.get('productId')

        if not user_id:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "userId is required."
            })

        if not product_id:
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "productId is required."
            })

        # Fetch the user and product objects
        user = get_object_or_404(users, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        # Check if the user already owns the product (optional, depends on your business logic)
        if User_Product_mapping.objects.filter(user=user, product=product).exists():
            return JsonResponse({
                "responseDto": None,
                "success": False,
                "error": "User already owns this product."
            })

        # Create a mapping entry
        user_product_mapping = User_Product_mapping.objects.create(user=user, product=product)

        # Construct the response data
        response_data = {
            "responseDto": {
                "productId": user_product_mapping.product.id,
                "productName": user_product_mapping.product.name
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
