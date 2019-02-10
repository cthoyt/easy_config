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
        assert len(dataclasses.fields(ExampleConfig)) + 1 == len(fields)  # add one because of submit button
        assert '<input id="number" name="number" required type="text" value="">' == str(fields[0])
        assert '<input id="bool_1" name="bool_1" type="checkbox" value="n">' == str(fields[1])
        assert '<input id="bool_2" name="bool_2" type="checkbox" value="n">' == str(fields[2])
        assert '<input id="bool_3" name="bool_3" type="checkbox" value="y">' == str(fields[3])
        assert '<input type="submit">' == str(fields[4])
