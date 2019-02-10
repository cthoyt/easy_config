# -*- coding: utf-8 -*-

"""An example web application showing form generation from EasyConfig."""

import flask
import flask_bootstrap
from flask import Flask
from flask_wtf import FlaskForm

from easy_config import EasyConfig
from easy_config.contrib.wtforms import form_from_config


class ExampleConfig(EasyConfig):
    """Example EasyConfig subclass to test with."""

    FILES = None
    NAME = 'MyProgram'

    bool_1: bool
    string_1: str
    # los: List[str]
    # date_1: date
    # datetime_1: datetime
    bool_2: bool = False
    bool_3: bool = True
    string_2: str = 'Hello'
    integer_3: int = 5
    float_1: float = 5.0


form_cls = form_from_config(ExampleConfig, base=FlaskForm)

app = Flask('test_app')
app.secret_key = 'test_app_key'
flask_bootstrap.Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Serve the example form."""
    form = form_cls()

    if not form.validate_on_submit():
        return flask.render_template('index.html', form=form)

    return '<table>' + '\n'.join(
        f'<tr>'
        f'<td>{field}</td>'
        f'<td>{getattr(form, field).data.__class__.__name__}</td>'
        f'<td>{getattr(form, field).data}</td>'
        f'</tr>'
        for field in form._fields
    ) + '</table>'


if __name__ == '__main__':
    app.run()
