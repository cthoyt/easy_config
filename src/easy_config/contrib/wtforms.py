"""Test the Flask-WTF wrapper."""

import dataclasses
from typing import Type

from easy_config import EasyConfig
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired

type_to_field = {
    str: StringField,
    int: IntegerField,
    bool: BooleanField,
}


def form_from_config(cls: Type[EasyConfig]):
    """Build a Flask-WTF form based on the given EasyConfig class."""
    attrs = {}

    for field in dataclasses.fields(cls):
        field_cls = type_to_field[field.type]
        attribute = field_cls(field.name, validators=[DataRequired()])
        if field.default is not dataclasses.MISSING:
            attribute.default = field.default
        attrs[field.name] = attribute

    return type(f'{cls.NAME}Form', (FlaskForm,), attrs)
