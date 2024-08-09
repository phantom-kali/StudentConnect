from django.core.exceptions import PermissionDenied
from functools import wraps

def premium_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_premium:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("This feature is only available to premium users.")
    return _wrapped_view