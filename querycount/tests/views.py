from django.db import connection
from django.http import HttpResponse


def empty(request):
    # An view with no DB queries.
    return HttpResponse("", content_type="text/plain")


def count_migrations(request):
    # A view that counts our existing migrations
    results = 0
    with connection.cursor() as cursor:
        cursor.execute("select count(*) from django_migrations")
        results = cursor.fetchone()[0]
    return HttpResponse(str(results), content_type="text/plain")
