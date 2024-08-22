from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
# Create your views here.


def users(request):
    return render(request, "users/users.html")


@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", username=member.username)
    return redirect("accounts:login")


def follow_detail(request, user_id):
    member = get_object_or_404(get_user_model(), pk=user_id)
    followers = member.followers.count()
    following = member.following.count()
    context = {
        "member": member,
        "followers": followers,
        "following": following,
    }
    return render(request, "users:profile", context)
