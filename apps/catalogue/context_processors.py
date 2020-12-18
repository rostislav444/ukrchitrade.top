from .models import Category


def categories(request):
    return {
        'root_categories' : Category.objects.filter(parent=None),
        'all_categories' :  Category.objects.all(),
    }
