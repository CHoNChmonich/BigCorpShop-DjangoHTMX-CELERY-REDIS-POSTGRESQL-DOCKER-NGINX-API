from rest_framework.pagination import PageNumberPagination


class StandartResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 15