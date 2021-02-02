# Django ecommerce
[![Maintainability](https://api.codeclimate.com/v1/badges/0617f3d247140be8a5a1/maintainability)](https://codeclimate.com/github/fnscoder/ecommerce/maintainability)
## Sobre as tecnologias
Você deverá criar um projeto Django que utilize a biblioteca Django Rest Framework para
servir um Web Service. Você pode adicionar outras bibliotecas se achar necessário, mas o
desenvolvimento das funcionalidades principais deve ser seu próprio.

## Escopo do projeto
Este projeto deve controlar o catálogo de produtos de um e-commerce. Cada produto
possui nome, descrição e preço. Sinta-se livre para adicionar outros campos (como foto ou
outros).
Cada produto está relacionado a uma ou nenhuma categoria. As categorias são simples e
possuem apenas um nome. Não é necessário adicionar sub-categorias, mas sinta-se livre
para fazê-lo.
Será necessário haver uma forma de autenticação para interagir com as APIs:
documente-a. O projeto deve fornecer uma forma de executar o CRUD para os produtos e
as categorias. Sinta-se encorajado a acrescentar recursos como paginação, filtragem de
resultados e similares.

## How to test
The project is available on [Heroku](https://ecommerce-fns.herokuapp.com/admin/)

* Documentation available on https://ecommerce-fns.herokuapp.com/docs/

## How to run the project locally
1. Clone repository
2. Create a virtualenv python 3.8
3. Activate your virtualenv
4. Install dependencies (gunicorn and psycopg2 are not required for development instance, only for deploy on heroku)
5. Configure the instance with .env file
6. Run the tests

```console
git clone git@github.com:fnscoder/ecommerce.git ecommerce
cd ecommerce
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/sample-env .env
python manage.py test
```

## Available endpoints

#### Register
POST `/auth/register/`
```console 
curl --location --request POST 'http://ecommerce-fns.herokuapp.com/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "my@email.com",
    "password": "my-password",
    "first_name": "MyName",
    "last_name": "LastName"
}' 
```

#### Login
POST `/auth/login/`
```console
curl --location --request POST 'http://ecommerce-fns.herokuapp.com/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "my@email.com",
    "password": "my-password",
}'
```
After the login you will receive the user auth_token. It must be included on the request header as `Authorization: Bearer <auth_token>`
#### Docs
GET `/docs/`

#### Users
GET `/users/`

GET, PUT, PATCH, DELETE `/users/<id>/`

#### Products
POST `/products/`
Create a product using a existent category
```console
curl --location --request POST 'http://ecommerce-fns.herokuapp.com/products/' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json' \
--data-raw '{
    "category": {"id": 1},
    "name": "bike",
    "description": "super bike",
    "price": 1500,
    "quantity": 10
}'
```
POST `/products/`
Create a product and create a category at same time
```console
curl --location --request POST 'http://ecommerce-fns.herokuapp.com/products/' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json' \
--data-raw '{
    "category": {"name": "new category"},
    "name": "bike",
    "description": "super bike",
    "price": 1500,
    "quantity": 10
}'
```

GET `/products/` (filters available - name, min_price and max_price)
```console
curl --location --request GET 'http://ecommerce-fns.herokuapp.com/products/?name=bike&min_price=100&max_price=2000' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json'
```
GET, PUT, PATCH, DELETE `/products/<id>/`
```console
curl --location --request GET 'http://ecommerce-fns.herokuapp.com/products/2/' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json'
```
#### Categories
GET, POST `/categories/`
```console
curl --location --request POST 'http://ecommerce-fns.herokuapp.com/categories/' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "food"
}'
```

GET, PUT, PATCH, DELETE `/categories/<id>/`
```console
curl --location --request GET 'http://ecommerce-fns.herokuapp.com/categories/1/' \
--header 'Authorization: Bearer c01fd75f5d3e913bd8af58d26cb539db7c43f687' \
--header 'Content-Type: application/json'
```

More information on the documentation page https://ecommerce-fns.herokuapp.com/docs/