from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Product
from django.db.models import Max, F, Min, Sum


def index(request):
    # ვიღებთ ყველა კატეგორიას რომელსაც მშობელი არ ჰყავს
    categories = Category.objects.all().filter(parent__isnull=True)
    categories_dict = {}
    categories_list = []
    for category_each in categories:
        # ვიღებთ ყველა ქვეკატეგორიას და წინასწარ მოგვაქვს პროდუქტები
        subcategories = (
            category_each
            .get_descendants(include_self=True)
            .prefetch_related("product_set")
        )
        counter = 0
        for subcategory in subcategories:
            # თითოეული ქვეკატეგორიისთვის ვითვლით
            # რამდენი პროდუქტი აქვს და ვინახავთ dictionary-ში
            sets = subcategory.product_set.all()
            counter += len(sets)
            categories_dict["category_name"] = category_each.category_name
            categories_dict["product_count"] = counter
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
    # ვიღებთ კატეგორიის ქვეკატეგორიებს
    subcategories = individual_category.get_descendants(include_self=True)

    # ვქმნი ცვლადებს რომელიც იქნება პროდუქტის კონტეინერი
    product_dict = {}
    product_list = []

    # ცვლადები რომლებიც დამეხმარება max და min მნიშვნელობების პოვნაში
    mx, all_sum, mx_value, mn_value, mn = 0, 0, None, None, 9999999999

    # აჯამებისთვის და რაოდენობისთვის
    summed, counter = 0, 0

    for subcategory in subcategories:
        # ყველა პროდუქტი ქვეკატეგორიაში
        sets = subcategory.product_set.all()

        # ვამატებთ ჯამურ ფასს ერთეული*ფასი და პროდუქტის ფასის ჯამს
        summed_set = sets.annotate(
            sum=F("product_quantity")*F("product_price"),
            sum_price=Sum("product_price")
        )

        # საშუალოს გამოსათვლელად გვჭირდება პროდუქტის ფასების ჯამი
        summed_agg = summed_set.aggregate(sum=Sum("sum_price"))
        if summed_agg["sum"]:
            # ვზრდით და ვინახავთ ჯამებს და რაოდენობებს
            summed += summed_agg["sum"]
            counter += len(summed_set)

        # ვპოულობთ min და max მარტივი გზით(ასევე პროდუქტებსაც ამ ფასებით)
        max_in_set = sets.aggregate(max=Max("product_price"))
        min_in_set = sets.aggregate(min=Min("product_price"))

        if max_in_set["max"] and max_in_set["max"] > mx:
            mx = max_in_set["max"]
            mx_value = sets.filter(product_price=mx).all()
        if min_in_set["min"] and min_in_set["min"] < mn:
            mn = min_in_set["min"]
            mn_value = sets.filter(product_price=mn).all()

        # თუ სეტი შეიცავს ელემენტებს მაშინ ავაწყოთ
        # პროდუქტისთვის საჭირო დიქშენერი
        if len(summed_set) > 0:
            for each_set in summed_set:
                product_dict["name"] = each_set.product_name
                product_dict["total_sum"] = each_set.sum
                product_dict["price"] = each_set.product_price
                product_dict["image"] = each_set.product_image
                product_dict["id"] = each_set.id

                # ეს გვჭირდება ყველა პროდუქტის ჯამური ღირებულება რომ დავთვალოთ
                all_sum += each_set.sum

                product_list.append(product_dict)
                product_dict = {}
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    products_objects = paginator.get_page(page_number)
    context = {
        'subcategories': subcategories,
        'category': individual_category,
        'products': product_list,
        'max_price': mx,
        'max_value': mx_value,
        'min_price': mn,
        'min_value': mn_value,
        'average': summed/counter,
        'all_sum': all_sum,
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
        'category_id': category_id
    }

    return render(request, "detail.html", context)
