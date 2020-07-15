def recursion_list(objects, objs=[]):
    for obj in objects:
        obj.childs = obj.__class__.objects.filter(parent=obj).order_by('name')
        if len(obj.childs) > 0:
            recursion_list(obj.childs, objs)
    return objects


def recursion(obj, objs=[]):
    if obj not in objs:
        objs.append(obj)
    for obj in obj.__class__.objects.filter(parent=obj):
        objs.append(obj)

        childs = obj.__class__.objects.filter(parent=obj)
        if len(childs) > 0:
            recursion(obj,objs)
    return objs