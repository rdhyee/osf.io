from django.utils import six
from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.core.paginator import InvalidPage, Paginator as DjangoPaginator

from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.utils.urls import (
    replace_query_param, remove_query_param
)

class JSONAPIPagination(pagination.PageNumberPagination):
    """
    Custom paginator that formats responses in a JSON-API compatible format.

    Properly handles pagination of embedded objects.

    """

    page_size_query_param = 'page[size]'

    def page_number_query(self, url, page_number):
        """
        Builds uri and adds page param.
        """
        url = self.request.build_absolute_uri(url)
        paginated_url = replace_query_param(url, self.page_query_param, page_number)

        if page_number == 1:
            return remove_query_param(paginated_url, self.page_query_param)

        return paginated_url

    def get_first_real_link(self, url):
        if not self.page.has_previous():
            return None
        return self.page_number_query(url, 1)

    def get_last_real_link(self, url):
        if not self.page.has_next():
            return None
        page_number = self.page.paginator.num_pages
        return self.page_number_query(url, page_number)

    def get_previous_real_link(self, url):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return self.page_number_query(url, page_number)

    def get_next_real_link(self, url):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return self.page_number_query(url, page_number)

    def get_paginated_response(self, data):
        """
        Formats paginated response in accordance with JSON API.

        Creates pagination links from the view_name if embedded resource,
        rather than the location used in the request.
        """
        kwargs = self.request.parser_context['kwargs'].copy()
        embedded = kwargs.pop('is_embedded', None)
        view_name = self.request.parser_context['view'].view_fqn
        reversed_url = None
        if embedded:
            reversed_url = reverse(view_name, kwargs=kwargs)

        response_dict = OrderedDict([
            ('data', data),
            ('links', OrderedDict([
                ('first', self.get_first_real_link(reversed_url)),
                ('last', self.get_last_real_link(reversed_url)),
                ('prev', self.get_previous_real_link(reversed_url)),
                ('next', self.get_next_real_link(reversed_url)),
                ('meta', OrderedDict([
                    ('total', self.page.paginator.count),
                    ('per_page', self.page.paginator.per_page),
                ]))
            ])),
        ])
        return Response(response_dict)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Custom pagination of queryset. Returns page object or `None` if not configured for view.

        If this is an embedded resource, returns first page, ignoring query params.
        """
        if request.parser_context['kwargs'].get('is_embedded'):
            page_size = self.get_page_size(request)
            if not page_size:
                return None
            paginator = DjangoPaginator(queryset, page_size)
            page_number = 1
            try:
                self.page = paginator.page(page_number)
            except InvalidPage as exc:
                msg = self.invalid_page_message.format(
                    page_number=page_number, message=six.text_type(exc)
                )
                raise NotFound(msg)

            if paginator.count > 1 and self.template is not None:
                # The browsable API should display pagination controls.
                self.display_page_controls = True

            self.request = request
            return list(self.page)

        else:
            return super(JSONAPIPagination, self).paginate_queryset(queryset, request, view=None)
