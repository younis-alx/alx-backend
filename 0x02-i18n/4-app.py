#!/usr/bin/env python3
'''Task 4: Force locale with URL parameter
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    '''Config class'''

    DEBUG = True
    LANGUAGES: list[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


def get_locale() -> str | None:
    """Retrieves the locale for a web page.

    Returns:
        str: best match
    """
    locale: str | None = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''default route

    Returns:
        html: homepage
    '''
    return render_template("4-index.html")

babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run()