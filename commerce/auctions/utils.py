def is_current_user(request, query_user, context):
    if request.user == query_user:
        is_current_user = True
        context["is_current_user"] = True
    return context