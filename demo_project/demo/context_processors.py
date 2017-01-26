def url_name(request):
    return dict(url_name=request.resolver_match.url_name)
