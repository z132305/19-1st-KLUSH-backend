from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models import Menu, MainCategory, SubCategory, Product, ProductImage, ProductOption


class MenuView(View):
    def get(self, request):
        try:
            main_category = MainCategory.objects.all()
            results = [
                {
                    "id"             : main.id,
                    "name"           : main.name,
                    "sub_categories" : [{"id" : sub.id, "name" : sub.name} for sub in main.subcategory_set.all()]
                }
                for main in main_category
            ]
            
            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class MainProductView(View):
    def get(self, request):
        try:
            PRODUCT_COUNT = 12
            product_list = Product.objects.all()[:PRODUCT_COUNT]
            results = [
                {
                    "id"          : product.id,
                    "image_url"   : product.productimage_set.filter(thumbnail_status=True).first().image_url,
                    "name"        : product.name,
                    "description" : product.hashtag,
                    "price"       : float(product.price)
                } 
                for product in product_list
            ]
        
            return JsonResponse({'results' : results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class ProductView(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('main_category_id')
            sub_category_id  = request.GET.get('sub_category_id')
            sort_type        = request.GET.get('sort')

            product_list     = Product.objects.filter(Q(sub_category=sub_category_id)|
                                                      Q(main_category=main_category_id))

            if(sort_type == "productPrice_asc"):
                product_list = product_list.order_by('price')
            
            elif(sort_type == "productPrice_desc"):
                product_list = product_list.order_by('-price')

            results = [
                {
                    "id"          : product.id,
                    "image_url"   : product.productimage_set.filter(thumbnail_status=True).first().image_url,
                    "name"        : product.name,
                    "description" : product.hashtag,
                    "price"       : float(product.price), 
                    "label"       : [{"type" : label.name, "color" : label.color} for label in product.label_set.all()]
                }
                for product in product_list
            ]
            return JsonResponse({'results' : results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
