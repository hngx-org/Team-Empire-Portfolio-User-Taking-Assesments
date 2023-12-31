# Zuri Portfolio Assessment Microservice

## 📝 Table of Contents

- [Zuri Portfolio Assessment Microservice](#zuri-portfolio-assessment-microservice)
  - [📝 Table of Contents](#-table-of-contents)
  - [🧐 About ](#-about-)
  - [🏁 Getting Started ](#-getting-started-)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
  - [🎈 Usage ](#-usage-)
    - [Windows](#windows)
    - [Linux and MacOS](#linux-and-macos)
  - [🚀 Deployment ](#-deployment-)

## 🧐 About <a name = "about"></a>
<!-- some fix -->
This is a microservice that is part of a larger project. It is responsible for handling the user taking assessments and grading them. It is written in Python and uses [FastAPI](fastapi.com) as the web framework. It uses a Postgres database to store the user's answers and the results of the assessment.

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

- Python 3.8 or higher
- All other dependencies are listed in the [requirements.txt file](requirements.txt).
- A Postgres database or credentials to a Postgres database

### Installing

1. Clone the repository
2. Create a virtual environment

  - For Linux and MacOS

     - For virtualenv
        ```bash
            make -v name_of_virtual_environment
        ```

     - For pipenv
        ```bash

            make -V
        ```

  - For Windows
    - For virtualenv
        ```bash
            make.bat v name_of_virtual_environment
        ```

     - For pipenv
        ```bash

            make.bat V
        ```
3. Install the dependencies

  - For Linux and MacOS
    ```bash
        make install
    ```
  - For Windows
    ```bash
        make.bat install
    ```

3. Create a `.env` file in the root directory of the project and add the following environment variables in [settings.py](app/settings.py) to the file:

```bash
DATABASE_URL=postgres://user:password@localhost:5432/database
```

## 🎈 Usage <a name="usage"></a>

To run the application, run the following command:

```bash
make
or
make run
```

To run the tests, run the following command:

### Windows

```bash
  make.bat test
```

### Linux and MacOS

```bash
make test
```

***[Documentation](http://localhost:8000/api) of the API is available at `http://localhost:8000/api`***


## 🚀 Deployment <a name = "deployment"></a>

You can deploy this application on serivces like [render.com](https://render.com/), [Heroku](https://www.heroku.com/), or [AWS](https://aws.amazon.com/). You can also deploy it on your own server.

To deploy it on your own server, you can use [gunicorn](https://gunicorn.org/) to run the application. You can also use [nginx](https://www.nginx.com/) as a reverse proxy to the application.

To deploy it on Heroku, you can follow the instructions [here](https://devcenter.heroku.com/articles/getting-started-with-python).

To deploy it on AWS, you can follow the instructions [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html).

To deploy it on render.com, you can follow the instructions [here](https://render.com/docs/deploy-fastapi).
