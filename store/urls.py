from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("category/", views.index, name="index"),
    path("category/<int:category_id>/products", views.category_listings, name="category_listings"),
    path("<int:category_id>/products", views.category_listings, name="category_listings"),
    path("<int:category_id>/products/<int:product_id>/", views.product, name="product"),
    path("category/<int:category_id>/products/<int:product_id>/", views.product, name="product"),
]
