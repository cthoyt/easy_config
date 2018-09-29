# -*- coding: utf-8 -*-

"""Test the Flask-WTF wrapper."""

import flask

from easy_config import EasyConfig
from easy_config.contrib.wtforms import form_from_config


def test_with_default():
    """Test building a form."""

    class ExampleConfig(EasyConfig):
        """Example EasyConfig subclass to test with."""

        FILES = None
        NAME = 'MyProgram'

        bool_1: bool
        bool_2: bool = True
        bool_3: bool = True

    form_cls = form_from_config(ExampleConfig)
    app = flask.Flask('test_app')

    with app.app_context():
        form = form_cls(csrf_enabled=False)
        for field in form:
            print(field)

        fields = list(form)
        assert 1 == len(fields)
        field = fields[0]
        assert str(field) == '<input id="number" name="number" required type="checkbox" value="y">'
