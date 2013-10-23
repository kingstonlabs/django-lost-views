import json

from django import http


def JsonResponse(data, status_code=200, cache_age=None):
    "A factory function that encodes the data into a HttpResponse."
    response = http.HttpResponse(
        json.dumps(data),
        mimetype="application/json",
    )
    response.status_code = status_code
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Headers'] = "Authorization"
    if cache_age:
        response['Cache-Control'] = "max-age=%i" % cache_age
    return response

