from django import forms


class CategoryAttributeValueForm(forms.ModelForm):
    model = 'catalogue_filters.CategoryAttributeValue'

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAttributeValueForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs.keys():
            print(kwargs)
            if kwargs['instance'] is not None:
                pass
                # categories = []
                # category = kwargs['instance'].category
                # while category != None:
                #     categories.append(category)
                #     category = category.parent
                # self.fields['selection'].queryset = Selection.objects.filter(parent__in=categories)