<!DOCTYPE html>
<html>
  <head>
    <style>
      body {
        background-image: url('demo/water3.jpg');
        background-size: cover;
        font-style: italic;
      }
      .content {
        background-color: rgba(); 
        padding: 20px;
        width: 50%;
        margin: 100px auto;
        font-family: Arial, sans-serif;
        font-size: 20px;
        line-height: 1.5;
        text-align: justify;
      }
      h1 {
        text-align: center;
      }
    </style>
  </head>
  <body class="content">
    <h1 style alright='center'>Page Analyzer</h1>
    <h2>### Description</h2>
    <p>Page analyzer is a simple web-application to get web-site base SEO characteristics.</p>
    <a href="https://codeclimate.com/github/BoCXoD-man/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/53ebfa71c65d245aabcb/maintainability" /></a>
    <a href="https://codeclimate.com/github/BoCXoD-man/python-project-83/test_coverage"><img src="https://api.codeclimate.com/v1/badges/53ebfa71c65d245aabcb/test_coverage" /></a>
    <a href="https://github.com/BoCXoD-man/python-project-83/workflows/hexlet-check/badge.svg"><img src="https://github.com/BoCXoD-man/python-project-83/workflows/hexlet-check/badge.svg" /></a>
    <a href="https://github.com/BoCXoD-man/python-project-83/actions/workflows/run_tests.yml"><img src="https://github.com/BoCXoD-man/python-project-83/actions/workflows/run_tests.yml/badge.svg" /></a>
    <a href="https://github.com/BoCXoD-man/python-project-83/actions/workflows/lint_check.yml"><img src="https://github.com/BoCXoD-man/python-project-83/actions/workflows/lint_check.yml/badge.svg" /></a>
    <p></p>
    <a href="https://python-project-83-production-372e.up.railway.app" target="_blank">You can take look at deployed app here.</a>
    <table>
      <thead>
        <tr>
          <th>Tool</th>
          <th>Version</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><a href="https://poetry.eustace.io" target="_blank">poetry</a></td>
          <td>^1.1.13</td>
          <td>Python dependency management and packaging made easy</td>
        </tr>
        <tr>
          <td><a href="https://flask.palletsprojects.com" target="_blank">flask</a></td>
          <td>^2.2.2</td>
          <td>Micro web framework written in Python</td>
        </tr>
        <tr>
          <td><a href="https://gunicorn.org" target="_blank">gunicorn</a></td>
          <td>^20.1.0</td>
          <td>Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX</td>
        </tr>
        <tr>
          <td><a href="https://requests.readthedocs.io" target="_blank">requests</a></td>
          <td>^2.28.2</td>
          <td>Elegant and simple HTTP library for Python</td>
        </tr>
        <tr>
          <td><a href="https://www.crummy.com/software/BeautifulSoup" target="_blank">bs4</a></td>
          <td>^4.11.2</td>
          <td>Python library for pulling data out of HTML and XML files</td>
        </tr>
              <tr>
          <td><a href="https://www.psycopg.org" target="_blank">psycopg2</a></td>
          <td>"^2.9.5"</td>
          <td>"Most popular PostgreSQL adapter for Python"</td>
        </tr>
              <tr>
          <td><a href="https://validators.readthedocs.io" target="_blank">validators</a></td>
          <td>"^0.20.0"</td>
          <td>"Python data validation"</td>
        </tr>
      </tbody>
    </table>
    <h2>#### How to install</h2>
    <pre>
      <span style="background-color:black;color:white;padding:5px;display:inline-block;">
        git clone https://github.com/BoCXoD-man/python-project-83 # clone repo
        cd python-project-83 # enter the directory
        # create .env file and add variables
        DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
        SECRET_KEY = '{your secret key}'
        # run commands from database.sql
        make install # install dependencies
        make dev # use local
        make start # or deploy with start command
      </span>
    </pre>
  </body>
</html>
