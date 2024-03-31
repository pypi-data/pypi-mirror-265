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

"""
Metadata that controls how a database property behaves. 
Each database property object contain the following; 
 - The ID of the property, usually a short string of random letters and symbols.
   Some automatically generated property types have special human-readable IDs. 
   For example, all Title properties have an ID of "title".name, id, and  key corresponding 
 - The name of the property as it appears in Notion.
 - A key corresponding with the value of type. The value is an object containing 
   type-specific configuration that controls the behavior of the property

NOTE: It is not possible to update a status database property in the current version of the Notion API. 
      Update these values from the Notion UI, instead.

https://developers.notion.com/reference/property-object
"""
from __future__ import annotations

from abc import ABCMeta
from typing import Optional, Sequence

from notion.properties.build import NotionObject
from notion.properties.options import FunctionFormat, NumberFormat, PropertyColor
from notion.properties.richtext import RichText

__all__: Sequence[str] = (
    "DatabaseDescription",
    "TitlePropertyObject",
    "RelationPropertyObject",
    "Option",
    "MultiSelectPropertyObject",
    "SelectPropertyObject",
    "NumberPropertyObject",
    "FormulaPropertyObject",
    "CheckboxPropertyObject",
    "PeoplePropertyObject",
    "PhoneNumberPropertyObject",
    "RichTextPropertyObject",
    "CreatedTimePropertyObject",
    "CreatedByPropertyObject",
    "LastEditedTimePropertyObject",
    "LastEditedByPropertyObject",
    "DatePropertyObject",
    "EmailPropertyObject",
    "FilesPropertyObject",
    "URLPropertyObject",
    "RollupPropertyObject",
)


class PropertyObject(metaclass=ABCMeta):
    def __init__(self, property_name: str) -> None:
        self.name = property_name


class DatabaseDescription(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, description: Sequence[RichText]) -> None:
        super().__init__()
        self.set("description", description)


class TitlePropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """
        A title database property controls the title that appears at the top of a page when a
        database row is opened. The title type object itself is empty; there is no additional configuration.

        NOTE: All databases require one, and only one, title property.
            The API throws errors if you send a request to Create a database without a title property,
            or if you attempt to Update a database to add or remove a title property.

        ---
        ### Title database property vs. database title
        A title database property is a type of column in a database.
        A database title defines the title of the database and is found on the database object.
        Every database requires both a database title and a title database property.

        https://developers.notion.com/reference/property-object#title
        """
        super().__init__(property_name=property_name)
        self.set("type", "title")
        self.set("title", {})


class _DualProperty(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, database_id: str, synced_property_name: str) -> None:
        """Internal use for RelationPropertyObject."""
        super().__init__()
        self.set("database_id", database_id)
        self.set("type", "dual_property")
        self.nest("dual_property", "synced_property_name", synced_property_name)


class _SingleProperty(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, database_id: str) -> None:
        """Internal use for RelationPropertyObject."""
        super().__init__()
        self.set("database_id", database_id)
        self.set("type", "single_property")
        self.set("single_property", {})


class RelationPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        property_name: str,
        relation_type: Optional[_DualProperty | _SingleProperty] = None,
    ) -> None:
        """
        Use classmethods:
         - `dual`
         - `single`

        https://developers.notion.com/reference/property-object#relation
        """
        super().__init__(property_name=property_name)
        self.set("type", "relation")
        self.set("relation", relation_type)

    @classmethod
    def dual(
        cls, property_name: str, database_id: str, synced_property_name: str
    ) -> RelationPropertyObject:
        """
        :param database_id: (required) The database that the relation property refers to.\
                             The corresponding linked page values must belong to the database in order to be valid.
        :param synced_property_name: (required) The name of the corresponding property that is\
                                      updated in the related database when this property is changed.
        """
        return cls(property_name, _DualProperty(database_id, synced_property_name))

    @classmethod
    def single(cls, property_name: str, database_id: str) -> RelationPropertyObject:
        """
        :param database_id: (required) The database that the relation property refers to.\
                             The corresponding linked page values must belong to the database in order to be valid.
        """
        return cls(property_name, _SingleProperty(database_id))


class Option(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, option_name: str, color: Optional[PropertyColor | str] = None, /
    ) -> None:
        """
        :param name: (required) The name of the option as it appears in the Notion UI.\
                      Note: Commas (",") are not valid for select values.
        :param color: (required) The color of the option as rendered in the Notion UI.\
                       Use `notion.properties.PropertyColor` for reference.
        """
        super().__init__()
        self.set("name", option_name)
        self.set("color", color) if color else None


class MultiSelectPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /, options: Sequence[Option]) -> None:
        """https://developers.notion.com/reference/property-object#multi-select"""
        super().__init__(property_name=property_name)
        self.set("type", "multi_select")
        self.nest("multi_select", "options", options)


class SelectPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /, options: Sequence[Option]) -> None:
        """https://developers.notion.com/reference/property-object#select"""
        super().__init__(property_name=property_name)
        self.set("type", "select")
        self.nest("select", "options", options)


class NumberPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        property_name: str,
        /,
        format: Optional[NumberFormat | str] = NumberFormat.number.value,
    ) -> None:
        """https://developers.notion.com/reference/property-object#number"""
        super().__init__(property_name=property_name)
        self.set("type", "number")
        self.nest("number", "format", format)


class FormulaPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /, expression: str) -> None:
        """
        :param expression: (required) The formula that is used to compute the values for this property.\
                            Refer to the Notion help center for information about formula syntax.
            
        https://developers.notion.com/reference/property-object#formula
        """
        super().__init__(property_name=property_name)
        self.set("type", "formula")
        self.nest("formula", "expression", expression)


class CheckboxPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#checkbox"""
        super().__init__(property_name=property_name)
        self.set("type", "checkbox")
        self.set("checkbox", {})


class PeoplePropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#people"""
        super().__init__(property_name=property_name)
        self.set("type", "people")
        self.set("people", {})


class PhoneNumberPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#phone-number"""
        super().__init__(property_name=property_name)
        self.set("type", "phone_number")
        self.set("phone_number", {})


class RichTextPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#rich-text"""
        super().__init__(property_name=property_name)
        self.set("type", "rich_text")
        self.set("rich_text", {})


class CreatedTimePropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#created-time"""
        super().__init__(property_name=property_name)
        self.set("type", "created_time")
        self.set("created_time", {})


class CreatedByPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#created-by"""
        super().__init__(property_name=property_name)
        self.set("type", "created_by")
        self.set("created_by", {})


class LastEditedTimePropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#last-edited-time"""
        super().__init__(property_name=property_name)
        self.set("type", "last_edited_time")
        self.set("last_edited_time", {})


class LastEditedByPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#last-edited-by"""
        super().__init__(property_name=property_name)
        self.set("type", "last_edited_by")
        self.set("last_edited_by", {})


class DatePropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#date"""
        super().__init__(property_name=property_name)
        self.set("type", "date")
        self.set("date", {})


class EmailPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#email"""
        super().__init__(property_name=property_name)
        self.set("type", "email")
        self.set("email", {})


class FilesPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#files"""
        super().__init__(property_name=property_name)
        self.set("type", "files")
        self.set("files", {})


class URLPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /) -> None:
        """https://developers.notion.com/reference/property-object#url"""
        super().__init__(property_name=property_name)
        self.set("type", "url")
        self.set("url", {})


class RollupPropertyObject(PropertyObject, NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        property_name: str,
        relation_property_name: str,
        rollup_property_name: str,
        function: Optional[FunctionFormat | str] = FunctionFormat.show_original.value,
    ) -> None:
        """https://developers.notion.com/reference/property-object#rollup"""
        super().__init__(property_name=property_name)
        self.set("type", "rollup")
        self.nest("rollup", "relation_property_name", relation_property_name)
        self.nest("rollup", "rollup_property_name", rollup_property_name)
        self.nest("rollup", "function", function)
