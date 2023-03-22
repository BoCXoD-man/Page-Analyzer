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
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

from page_analyzer.checks import (validate_url,
                                  get_url_data,
                                  get_checks_by_id,
                                  add_check,
                                  get_urls_by_name
                                  )


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


def get_connect_db():
    """
    CLI is a utility.
    :return: the connection to the database.
    """

    conn = connect(DATABASE_URL)
    return conn


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

    urls = get_all_urls()

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

    url = request.form.get('url')
    check = validate_url(url)

    url = check['url']
    error = check['error']

    if error == 'exists':
        id_url = get_urls_by_name(url)['id']
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for(
            'url_show',
            id_url=id_url
        ))

    elif error:
        flash('Некорректный URL', 'alert-danger')
        if error == 'zero':
            flash('URL обязателен', 'alert-danger')
        elif error == 'length':
            flash('URL превышает 255 символов', 'alert-danger')
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
        add_site(site)
        id_url = get_urls_by_name(url)['id']
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for(
            'url_show',
            id_url=id_url
        ))


@app.route('/urls/<int:id_url>')
def url_show(id_url):
    """
    Render one URL page containing its parsed check data.
    :param id_: URL id.
    :return: Render page or raise 404 error.
    """

    try:
        url = get_urls_by_id(id_url)
        checks = get_checks_by_id(id_url)

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


@app.post('/urls/<int:id_url>/checks')
def url_check(id_url):
    """
    Check requested URL. Add data to db or raise error.
    :param id_url: URL id.
    :return: Redirect to one URL show page adding check data to db or returning
    error if an error occured during check.
    """

    url = get_urls_by_id(id_url)['name']

    try:
        check = get_url_data(url)

        check['url_id'] = id_url
        check['checked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_check(check)

        flash('Страница успешно проверена', 'alert-success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')

    return redirect(url_for(
        'url_show',
        id_url=id_url
    ))


def add_site(site: dict) -> None:
    """
    Insert into database new URL.
    Tables: urls
    :param site: Dict containing URL and its creation date.
    """

    conn = get_connect_db()
    with conn.cursor() as cur:
        q_insert = '''INSERT
        INTO urls (name, created_at)
        VALUES (%s, %s)'''
        cur.execute(q_insert, (
            site['url'],
            site['created_at']
        ))
        conn.commit()
    conn.close()


def get_all_urls() -> dict:
    """
    Query the database for all added URLs. Return only the last check info.
    Tables: urls, url_checks
    :return: Dict of all urls, its id's, last check dates and status codes.
    """

    conn = get_connect_db()
    conn.autocommit = True
    curs = conn.cursor(cursor_factory=RealDictCursor)
    curs.execute(
        "SELECT urls.id, urls.name, url_checks.created_at, "
        "url_checks.status_code FROM urls LEFT JOIN "
        "(SELECT * FROM url_checks WHERE id IN "
        "(SELECT MAX(id) as id FROM url_checks GROUP BY url_id)) "
        "AS url_checks ON urls.id = url_checks.url_id "
        "ORDER BY urls.id DESC")
    data_urls = curs.fetchall()
    conn.close()
    return data_urls


def get_urls_by_id(id_url: int) -> dict:
    """
    Query the database for one URL data based on its id.
    Tables: urls
    :param id_url: URL id.
    :return: Dict containing one url data: id, name, creation date.
    """

    conn = get_connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        q_select = '''SELECT *
        FROM urls WHERE id=(%s)'''
        cur.execute(q_select, [id_url])
        urls = cur.fetchone()
    conn.close()

    return urls


if __name__ == '__main__':
    app.run()
