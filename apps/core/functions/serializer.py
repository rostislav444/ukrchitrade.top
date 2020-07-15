def getSerializerLabels(serializer):
    labels = {}
    for name, field in serializer.get_fields().items():
        labels[name] = field.label or name.replace("_", " ").capitalize() 
    return labels