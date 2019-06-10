import base64

from django import forms
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from .models import Item, Review


class GoodForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.CharField(max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)


# r = requests.post(url, headers={'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'})


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        coded_str = request.headers['authorization'].split()[1]
        decoded_str = base64.b64decode(coded_str).decode('utf-8')
        username, password = decoded_str.split(':')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                return JsonResponse({}, status=201)
            return JsonResponse({}, status=403)
        return JsonResponse({}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        form = ReviewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['item'] = item
            Review.objects.create(**cd)
        return JsonResponse(status=400, data={})


class GetItemView(View):
    """View для получения информации о товаре.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.prefetch_related('review_set').get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        item_dict = model_to_dict(item)
        item_reviews = [model_to_dict(x) for x in item.review_set.all()]
        item_reviews = sorted(
            item_reviews, key=lambda review: review['id'], reverse=True)[:5]
        for review in item_reviews:
            review.pop('item', None)
        item_dict['reviews'] = item_reviews
        return JsonResponse(item_dict, status=200)
