def search(request):
    search_query = request.GET.get("search")
    return search_query
