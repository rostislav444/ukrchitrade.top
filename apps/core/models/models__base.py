from django.db import models
from apps.core.models import Translation, NameSlug


class Country(NameSlug, Translation):
    pass
