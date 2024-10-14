from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Product
from django.db.models import Max, F, Min, Sum, Count, Avg


def index(request):
    # ვიღებთ ყველა კატეგორიას რომელსაც მშობელი არ ჰყავს
    categories = Category.objects.all().filter(parent__isnull=True)
    categories_dict = {}
    categories_list = []
    for category_each in categories:
        # ვიღებთ ყველა ქვეკატეგორიას
        subcategories = (
            category_each
            .get_descendants(include_self=True)
        )
        # ვამატებთ count-ს რომელიც დაითვლის თითოეული ქვეკატეგორიის პროდუქტების რაოდენობას
        product_counted = subcategories.annotate(products_count=Count("product"))

        # ვჯამავთ თითოეულ ქვეკატეგორიაში products_count ველის მნიშვნელობებს
        total_product_count = product_counted.aggregate(total_count=Sum("products_count"))

        categories_dict["category_name"] = category_each.category_name
        categories_dict["product_count"] = total_product_count["total_count"]
        categories_dict["id"] = category_each.id
        categories_list.append(categories_dict)
        categories_dict = {}
    context = {
        'categories': categories_list,
    }
    return render(request, "index.html", context)


def category_listings(request, category_id):
    # ვიღებთ კატეგორიას ID-ის მიხედვით
    individual_category = Category.objects.get(id=category_id)
    # ვიღებთ კატეგორიის ქვეკატეგორიებს და წინასწარ მოგვაქვს პროდუქტები დასარენდერებლად
    subcategories = individual_category.get_descendants(include_self=True)

    # ყველაზე ძვირიანი პროდუქტის ფასი
    most_expensive = subcategories.aggregate(max_price=Max("product__product_price"))
    # ყველაზე იაფიანი პროდუქტის ფასი
    cheapest = subcategories.aggregate(min_price=Min("product__product_price"))
    # საშუალო ფასი
    average_price = subcategories.aggregate(avg_price=Avg("product__product_price"))
    # ვჯამავთ ყველა პროდუქტის ჯამი*რაოდენობას
    sum_total = subcategories.annotate(sum_each=F("product__product_quantity")*F("product__product_price"))
    subtotal = sum_total.aggregate(subtotal=Sum("sum_each"))

    product_dict = {}
    product_list = []
    for subcategory in subcategories:
        # ყველა პროდუქტი ქვეკატეგორიაში
        sets = subcategory.product_set.all()

        # თითოეული პროდუქტის ფასი*რაოდენობა
        sets = sets.annotate(sum=F("product_quantity")*F("product_price"))
        for each_set in sets:
            product_dict["name"] = each_set.product_name
            product_dict["total_sum"] = each_set.sum
            product_dict["price"] = each_set.product_price
            product_dict["image"] = each_set.product_image
            product_dict["id"] = each_set.id
            product_list.append(product_dict)
            product_dict = {}

    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    products_objects = paginator.get_page(page_number)
    context = {
        'subcategories': subcategories,
        'category': individual_category,
        'products': product_list,
        'max_price': most_expensive["max_price"],
        'min_price': cheapest["min_price"],
        'average': round(average_price["avg_price"]),
        'all_sum': subtotal["subtotal"],
        'products_objects': products_objects,
    }
    return render(request, "category.html", context)


def product(request, category_id, product_id):
    product_element = Product.objects.get(id=product_id)
    product_dictionary = {
        "product_name": product_element.product_name,
        "product_description": product_element.product_description,
        "product_price": product_element.product_price,
        "product_quantity": product_element.product_quantity
    }
    if product_element.product_image:
        image = request.build_absolute_uri(product_element.product_image.url)
    else:
        image = None
    product_dictionary["product_image"] = image

    categories = (
        product_element
        .product_category
        .all()
        .get_ancestors(include_self=True).all()
    )
    category_list = []
    for cat in categories:
        cat_dict = {
            "id": cat.id,
            "name": cat.category_name,
        }
        category_list.append(cat_dict)

    product_dictionary["product_categories"] = category_list
    context = {
        'product': product_dictionary,
        'product_id': product_id,
        'category_id': category_id
    }

    return render(request, "detail.html", context)
