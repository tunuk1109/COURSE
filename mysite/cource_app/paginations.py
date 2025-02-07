from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5

class ExamPagination(PageNumberPagination):
    page_size = 3


class CategoryPagination(PageNumberPagination):
    page_size = 5