from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from store.models import Category, Product

# Register your models here.


admin.site.register(
    Category,
    # MPTTModelAdmin,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    )
)
admin.site.register(Product)
