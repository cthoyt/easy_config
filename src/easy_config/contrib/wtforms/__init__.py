# -*- coding: utf-8 -*-

"""A wrapper for generating HTML forms from dataclasses with a :mod:`wtforms`."""

import dataclasses
import logging
from datetime import date, datetime
from typing import Dict, List, Type

import wtforms
from wtforms import (
    BooleanField, DateField, DateTimeField, FloatField, Form, IntegerField, StringField, SubmitField,
)
from wtforms.validators import DataRequired, InputRequired

from easy_config import EasyConfig


__all__ = [
    'form_from_config',
    'WtFormsProcessor',
]

logger = logging.getLogger(__name__)


def form_from_config(cls: Type[EasyConfig], base: Type[Form] = Form) -> Type[Form]:
    """Build a Flask-WTF form based on the given EasyConfig class.

    `base` can be replaced with :class:`flask_wtf.FlaskForm` as well.
    """
    processor = WtFormsProcessor(cls)
    return processor.process(base)


class WtFormsProcessor:
    """Process a dataclass."""

    def __init__(self, dataclass: dataclasses.dataclass) -> None:  # noqa: D107
        self.dataclass = dataclass

        #: A conversion dictionary from Python types used in the dataclass to WTForms field types that can be amended
        self.type_to_field: Dict[type, wtforms.Field] = {
            str: StringField,
            int: IntegerField,
            bool: BooleanField,
            float: FloatField,
            date: DateField,
            datetime: DateTimeField,
        }

    def process(self, base: Type[Form] = Form) -> Type[Form]:
        """Generate a subclass of :class:`wtforms.Form` from the enclosed :class:`easy_config.EasyConfig` class."""
        attrs = {}

        for dataclass_field in dataclasses.fields(self.dataclass):  # type: ignore
            if isinstance(dataclass_field.type, List.__class__):
                logger.warning(f'Can not add {dataclass_field.name}: list fields are not yet supported')
                continue
                # form_field = self.process_list_field(dataclass_field)
            else:
                form_field = self.process_simple_field(dataclass_field)

            attrs[dataclass_field.name] = form_field

        attrs['submit'] = SubmitField()

        return type(f'{self.dataclass.NAME}Form', (base,), attrs)  # type: ignore

    def process_simple_field(self, dataclass_field: dataclasses.Field) -> wtforms.Field:
        """Generate a :py:class`wtforms.Field` from a :py:class:`dataclass.Field`."""
        form_field_cls: wtforms.Field = self.type_to_field[dataclass_field.type]

        if dataclass_field.default is not dataclasses.MISSING:
            default = dataclass_field.default
        elif dataclass_field.type is bool:  # default for boolean is automatically false
            default = False
        else:
            default = None

        if dataclass_field.type is bool:
            validators = []
        else:
            validators = [DataRequired()]

        form_field = form_field_cls(
            label=dataclass_field.name.replace('_', ' ').capitalize(),
            validators=validators,
            default=default,
        )
        return form_field

    def process_list_field(self, dataclass_field: dataclasses.Field) -> wtforms.FieldList:
        """Generate a :py:class`wtforms.FieldList` from a :py:class:`dataclass.Field`."""
        arg: type = dataclass_field.type.__args__[0]
        form_field_cls = self.type_to_field[arg]
        form_field = form_field_cls(dataclass_field.name, validators=[InputRequired()])
        list_form_field = _get_list_field(form_field)
        return list_form_field


def _get_list_field(field: wtforms.Field) -> wtforms.Field:
    raise NotImplementedError
