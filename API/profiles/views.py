from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

User = get_user_model()


@login_required
def profile_list_view(request, *args, **kwargs):
    qs = User.objects.filter(is_active=True).values()
    qs = [entry for entry in qs]
    qs = {"data": qs, "title": "Profile List"}
    return render(request, "profiles/list.html", context=qs)


@login_required
def profile_view(request, username: str = None, *args, **kwargs):
    pr_user_obj = get_object_or_404(User, username=username)
    return HttpResponse(f"Hello {pr_user_obj.username} with id {pr_user_obj.id}!")


@login_required
def details_profile_view(request, username: str = None, *args, **kwargs):
    user = request.user
    print(
        user.has_perm("subscriptions.enterprise"),
        user.has_perm("subscriptions.standard"),
        user.has_perm("subscriptions.free"),
    )
    pr_user_obj = get_object_or_404(User, username=username)
    is_me = (
        pr_user_obj == user
    )  # checks if the user who hits the endpoint is present in the db or not
    return render(
        request,
        "profiles/details.html",
        context={
            "object": pr_user_obj,
            "instance": pr_user_obj,
            "owner": is_me,
            "title": "Profile",
        },
    )
