# -*- coding: utf-8 -*-

"""Test the :mod:`wtforms` wrapper."""

import dataclasses

import flask
from flask_wtf import FlaskForm

from easy_config import EasyConfig
from easy_config.contrib.wtforms import WtFormsProcessor, form_from_config


def _get_only_field(cls):
    return list(dataclasses.fields(cls))[0]


def test_int():  # noqa: D202
    """Test a dataclass with only a non-default integer."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        number: int

    processor = WtFormsProcessor(ExampleConfig)
    field = _get_only_field(ExampleConfig)
    x = processor.process_simple_field(field)
    assert 'number' == x.args[0]


def test_with_default():  # noqa: D202
    """Test building a form."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        number: int
        bool_1: bool
        bool_2: bool = False
        bool_3: bool = True

    form_cls = form_from_config(ExampleConfig, base=FlaskForm)
    form_cls.Meta.csrf = False
    app = flask.Flask('test_app')

    with app.app_context():
        form = form_cls()
        fields = list(form)
        assert 4 == len(fields) - 1  # because of submit button
        assert str(fields[0]) == '<input id="number" name="number" required type="text" value="">'
        assert str(fields[1]) == '<input id="bool_1" name="bool_1" required type="checkbox" value="n">'
        assert str(fields[2]) == '<input id="bool_2" name="bool_2" required type="checkbox" value="n">'
        assert str(fields[3]) == '<input id="bool_3" name="bool_3" required type="checkbox" value="y">'
