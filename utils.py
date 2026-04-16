from django.core.paginator import Paginator
from django.http import HttpRequest

from constants.limits import PaginationLimit


def paginate(
    request: HttpRequest, queryset, per_page: int = PaginationLimit.PROJECTS_PER_PAGE
):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
