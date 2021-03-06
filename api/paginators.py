from rest_framework.pagination import CursorPagination


class CursorSetPagination(CursorPagination):
	page_size = 4
	page_size_query_param = 'page_size'
	ordering = '-created_at'