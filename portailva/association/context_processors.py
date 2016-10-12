def my_associations(request):
    if request.user is None or not request.user.is_authenticated():
        associations = []
    else:
        associations = request.user.associations.all()

    return {'my_associations': associations}