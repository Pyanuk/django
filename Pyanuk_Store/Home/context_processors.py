from .models import Users

def current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            return {'current_user': user}
        except Users.DoesNotExist:
            return {'current_user': None}
    return {'current_user': None}