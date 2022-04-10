from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def server_error_view(request):
    return render(request, "500.html", status=500)


def permission_denied_view(request, exception):
    return render(request, "403.html", status=403)
