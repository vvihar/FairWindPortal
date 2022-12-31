from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if (
            not request.user.is_authenticated
            and request.path != reverse("accounts:login")
            and request.path != reverse("accounts:logout")
            and request.path != reverse("home")
            and not request.path.startswith(reverse("calendar:integration"))
            and request.path != reverse("calendar:integration")
            and not request.path.startswith("/admin/")
        ):
            return HttpResponseRedirect(
                reverse("accounts:login") + "?next=" + request.path
            )
        return response
