from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.request = request  # Set the request context
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied
        return render(self.request, '403.html', status=403)
