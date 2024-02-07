#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
import pytz
from typing import Union, Dict, Any
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES: list[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users: dict[int, Any] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieves a user based on a user id.
    """
    login_id: str = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Performs some routines before each request's resolution.
    """
    user: Dict[int, Any] | None = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.
    """
    queries: list[str] = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    locale: str = query_table.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    user_details: Any | None = getattr(g, 'user', None)
    if user_details and user_details['locale'] in app.config["LANGUAGES"]:
        return user_details['locale']
    header_locale: str = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return app.config['BABEL_DEFAULT_LOCALE']


def get_timezone() -> str | None:
    """Retrieves the timezone for a web page.
    """
    timezone: str = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """The home/index page.
    """
    g.time = format_datetime()
    return render_template('index.html')

babel.init_app(app, locale_selector=get_locale)


if __name__ == '__main__':
    app.run()
