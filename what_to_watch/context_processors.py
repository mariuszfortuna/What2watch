from django.contrib.auth.decorators import user_passes_test


#Check if user is in Moderators group
def user_is_moderator(user):
    return user.groups.filter(name='Moderators').exists()


#The user_is_moderator variable will be available in the context of each template.
def moderator_context(request):
    return {'user_is_moderator': user_is_moderator(request.user)}