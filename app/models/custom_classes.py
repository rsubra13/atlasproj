"""
Custom classes
"""

# from app import db
from jinja2 import Markup
from math import ceil
# from datetime import datetime, timedelta


class MomentJs(object):
    """
    Custom MomentJS Library for handling timestamps.
    """
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\n document.write(moment(\"%s\").%s);\n \
                      </script>" %
                     (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")


class Pagination(object):
    """Helper for creating paging naviagtion."""
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        if not hasattr(self, '_pages'):
            self._pages = int(ceil(self.total_count / float(self.per_page)))

        return self._pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
