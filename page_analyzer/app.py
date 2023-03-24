from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   get_flashed_messages
                   )
from dotenv import load_dotenv
from datetime import datetime
import requests
import os

from page_analyzer.html import get_url_data
from page_analyzer.url_valid import validate_url
from page_analyzer.db import (get_connection,
                              close,
                              get_urls_by_id,
                              get_urls_by_name,
                              get_all_urls,
                              add_site,
                              add_check,
                              get_checks_by_id)


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(error):
    """
    Render 404 error page if the requested page is missing.
    :return: Render 404.html.
    """

    return render_template(
        '404.html'
    ), 404


@app.route('/')
def index():
    """
    Render index.html.
    :return: Render index.html.
    """

    return render_template(
        'index.html',
    )


@app.get('/urls')
def urls_get():
    """
    Render all added URLs page with last check dates and status codes if any.
    :return: Render all URLs page.
    """

    conn = get_connection()
    urls = get_all_urls(conn)
    close(conn)

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        urls=urls,
        messages=messages
    )


@app.post('/urls')
def urls_post():
    """
    Add new URL. Check if there is one provided. Validate the URL.
    Add it to db if this URL isn't already there. Raise an error if any occurs.
    :return: Redirect to one URL page if new URL added or it is already in db.
    Render index page with flash error if any.
    """

    # 1 step of validation
    url = request.form.get('url')
    check = validate_url(url)

    # 2 step of validation
    conn = get_connection()
    found = get_urls_by_name(check['url'], conn)
    close(conn)

    if found:
        check['error'] = 'exists'

    # Total validation:
    url = check['url']
    error = check['error']

    if error == 'exists':
        conn = get_connection()
        url_id_ = get_urls_by_name(url, conn)['id']
        close(conn)
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for(
            'url_show',
            url_id_=url_id_
        ))
    elif error == 'zero':
        flash('Некорректный URL', 'alert-danger')
        flash('URL обязателен', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages
        ), 422
    elif error == 'length':
        flash('Некорректный URL', 'alert-danger')
        flash('URL превышает 255 символов', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages
        ), 422
    elif error == 'invalid':
        flash('Некорректный URL', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages
        ), 422
    else:
        site = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        conn = get_connection()
        add_site(site, conn)
        close(conn)

        conn = get_connection
        url_id_ = get_urls_by_name(url, conn)['id']
        close(conn)

        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for(
            'url_show',
            url_id_=url_id_
        ))


@app.route('/urls/<int:url_id_>')
def url_show(url_id_):
    """
    Render one URL page containing its parsed check data.
    :param url_id_: URL id.
    :return: Render page or raise 404 error.
    """

    try:
        conn = get_connection()
        url = get_urls_by_id(url_id_, conn)
        close(conn)

        conn = get_connection()
        checks = get_checks_by_id(url_id_, conn)
        close(conn)

        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'show.html',
            url=url,
            checks=checks,
            messages=messages
        )
    except IndexError:
        return render_template(
            '404.html'
        ), 404


@app.post('/urls/<int:url_id_>/checks')
def url_check(url_id_):
    """
    Check requested URL. Add data to db or raise error.
    :param url_id_: URL id.
    :return: Redirect to one URL show page adding check data to db or returning
    error if an error occured during check.
    """

    conn = get_connection()
    url = get_urls_by_id(url_id_, conn)['name']
    close(conn)

    try:
        check = get_url_data(url)

        check['url_id'] = url_id_
        check['checked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        add_check(check, conn)
        close(conn)

        flash('Страница успешно проверена', 'alert-success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')

    return redirect(url_for(
        'url_show',
        url_id_=url_id_
    ))


if __name__ == '__main__':
    app.run()
