# -*- coding: utf-8 -*-

"""A wrapper for generating forms with a :mod:`wtforms`."""

import dataclasses
from datetime import date, datetime
from typing import List, Type

from wtforms import BooleanField, DateField, DateTimeField, FieldList, FloatField, Form, IntegerField, StringField
from wtforms.validators import DataRequired

from easy_config import EasyConfig

__all__ = [
    'form_from_config',
]

type_to_field = {
    str: StringField,
    int: IntegerField,
    bool: BooleanField,
    float: FloatField,
    date: DateField,
    datetime: DateTimeField,
}


def form_from_config(cls: Type[EasyConfig], base: Type[Form] = Form) -> Type[Form]:
    """Build a Flask-WTF form based on the given EasyConfig class.

    `base` can be replaced with :class:`flask_wtf.FlaskForm` as well.
    """
    attrs = {}

    for dataclass_field in dataclasses.fields(cls):
        if isinstance(dataclass_field.type, List.__class__):
            arg = dataclass_field.type.__args__[0]
            form_field_cls = type_to_field[arg]
            form_field = FieldList(form_field_cls(dataclass_field.name, validators=[DataRequired()]))
        else:
            form_field_cls = type_to_field[dataclass_field.type]
            form_field = form_field_cls(dataclass_field.name, validators=[DataRequired()])

        if dataclass_field.default is not dataclasses.MISSING:
            form_field.default = dataclass_field.default
        attrs[dataclass_field.name] = form_field

    return type(f'{cls.NAME}Form', (base,), attrs)
