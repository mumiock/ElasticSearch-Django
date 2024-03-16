<div align="center">
<h1>
  ElasticSearch-Django
</h1>
<div>

**ElasticSearch-Django is an innovative api application for ElasticSearch and Django interaction.**

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
<br>

</div>
</div>

## <div align="center">Overview</div>

This guide will walk you through the steps to install and run the ElasticSearch-Django application. Also includes additional information necessary for local testing or development of the project.

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Additional Information](#additional-information)

### About the Project

#### **Prerequisites**

Before you get started, ensure you have the following installed on your system:

- Python (**version 3.7 or higher**)
- Python-pip
- Docker

### Getting Started

#### **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/mumiock/ElasticSearch-Django.git
   cd ElasticSearch-Django
   ```

2. Create a virtual environment and activate it (**optional but recommended**):

   ```bash
   python -m venv venv
   ```

   If the PATH variable does not contain the **python** executable path. Try the **python3** command:

   ```bash
   python3 -m venv venv
   ```

   Activate virtual environment:

   For Unix based (Linux & macOS) systems:

   ```bash
   source venv/bin/activate
   ```

   For Windows based systems:

   ```bash
   .\venv\Scripts\activate
   ```

3. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   If the python environment does not contain the **pip** executable. Try the **pip3** command:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Prepare the Database for local development(**optional**): :

   ```bash
   python manage.py makemigrations
   python manage.py makemigrations elastic_search_app
   python manage.py migrate
   ```

#### **Usage**

1. Start the Django app using terminal:

   If you are in development:

   ```bash
   python manage.py runserver
   ```

   If you are in production:

   ```bash
   docker compose up --build -d
   ```

2. Access the Django app in your web browser at http://localhost:8000 or your ip server.

## Additional Information

For more detailed information on Django, Docker; consult their respective documentation:

- [Django Documentation](https://docs.djangoproject.com/en/5.0/).

- [Docker Documentation](https://docs.docker.com/).
