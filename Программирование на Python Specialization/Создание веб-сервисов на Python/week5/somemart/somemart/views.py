import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review


class AddItemView(View):
    """View для создания товара."""
    # api/v1/goods/

    def post(self, request):
        # Здесь должен быть ваш код
        return JsonResponse(data, status=201)


class PostReviewView(View):
    """View для создания отзыва о товаре."""
    # api/v1/goods/<int:item_id>/reviews/

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(data, status=201)


class GetItemView(View):
    # api/v1/goods/<int:item_id>/
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(data, status=200)
