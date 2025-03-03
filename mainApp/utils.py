from django.contrib import auth
from django.contrib.auth.models import Group

# ------------------------ Verify user group --------------------------------------
def verify_user_group(request,group_name:str):
    if not request.user.groups.filter(name=group_name).exists():
        auth.logout(request)
        
def add_user_to_group(request,group_name:str):
    group = Group.objects.get(name=group_name)
    group.user_set.add(request.user)
