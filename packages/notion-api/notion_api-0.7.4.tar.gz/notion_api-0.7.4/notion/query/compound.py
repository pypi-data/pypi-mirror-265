# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

from typing import Sequence

from notion.properties.build import NotionObject
from notion.query.propfilter import PropertyFilter
from notion.query.timestamp import TimestampFilter

__all__: Sequence[str] = ("CompoundFilter",)


class CompoundFilter(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        """Create a separate CompoundFilter object to nest an `and` operator inside another `and` or `or`.

        :method: _and() combine all filters in an `and` grouping.
        :method: _or() combine all filters in an `or` grouping.

        https://developers.notion.com/reference/post-database-query-filter#compound-filter-object
        """
        super().__init__()

    def _and(
        self, *filters: PropertyFilter | CompoundFilter | TimestampFilter
    ) -> CompoundFilter:
        """
        Example compound filter conditions
        https://developers.notion.com/reference/post-database-query-filter#example-compound-filter-conditions
        """
        filter_objects = [f["filter"] if "filter" in f else f for f in filters]
        self.nest("filter", "and", filter_objects)
        return self

    def _or(
        self, *filters: PropertyFilter | CompoundFilter | TimestampFilter
    ) -> CompoundFilter:
        """
        Example compound filter conditions
        https://developers.notion.com/reference/post-database-query-filter#example-compound-filter-conditions
        """
        filter_objects = [f["filter"] if "filter" in f else f for f in filters]
        self.nest("filter", "or", filter_objects)
        return self
