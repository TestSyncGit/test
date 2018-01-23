# Billevent API

Billevent is the online ticket office manager for the BdE INSA Lyon student
union. It allows to sells tickets for events, accept payments, issue and
control tickets.

## Technologies

This application has no frontend, it's an API accessible with a REST scheme.

The API is driven by the Django REST Framework and frontend applications
connects to it directly (eventualy with authentication tokens)

The database used on the project is PostgreSQL but on a local developer
computer it can fit with a SQLite DB.

When application is ready, it is deployed using Docker on a pre-prod and,
if code and tests (no one written currently) are OK, then deployed on
production. It's a CI/CD scheme managed by GitLab.

## Setup

### Side services

- A database service like PostgreSQL or SQLite (never tried for MySQL)
- A broker message service like RabbitMQ

### Environment Variables

```dotenv
API_URL=https://your.api.domain.fr
BROKER_URL=amqp://guest:guest@rabbitmq-server:5672/
DATABASE_URL=postgres://postgres@postgres-server/billevent
DEFAULT_FROM_EMAIL=BdE INSA Lyon <billetterie@bde-insa-lyon.fr>
DOMAINS=your.api.domain.fr,your.frontend.domain.fr,your.manager.domain.fr
ENV=development
FORWARDED_ALLOW_IPS=*
FRONTEND_URL=https://your.frontend.domain.fr
HOST=localhost
MAILGUN_API_KEY=key-YOURAPIKEY
MAILGUN_DOMAIN=your.api.domain.fr
MERCANET_INTERFACE_VERSION=IR_WS_2.18
MERCANET_KEY_VERSION=1
MERCANET_MERCHANT_ID=<the merchant id>
MERCANET_SECRET_KEY=<the secret key>
MERCANET_REPONSE_AUTO_URL=https://your.api.domain.fr/pay/auto/
MERCANET_URL=https://payment-webinit-mercanet.test.sips-atos.com/rs-services/v2/paymentInit
```

### Simple launch (development only)

Write all environment variables to a `.env` file on the root of project

Then simply run `python manage.py runserver`

## Licence

This project is under GNU AGPL 3.0 License

### Contributors
```
Philippe VIENNE <philippegeek@gmail.com>
Alban PRATS
Jean RIBES
Hugo REYMOND
François LALLEVE
Gabriel AUGENDRE
```
