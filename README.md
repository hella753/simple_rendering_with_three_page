# Simple HTML Rendering With 3 Page

## Description
The Musical instruments store with products ordered in categories. The project has 3 pages: one for categories, 
one for products, one for product detail. Uses HTML templates and has a simple design. It also provides basic 
statistical analysis per category.
The Project uses Django and sqlite3 database.

Project Structure:
```
simple_rendering_with_three_page/
├── media
├── simple_rendering_with_three_page
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   ├── static
│   │   ├── store
│   │   │   ├── style.css
│   ├── templates
│   │   ├── category.html
│   │   ├── detail.html
│   │   ├── index.html
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

```

Database name: `db` <br>
Tables created: `store_category`, `store_product`, `store_product_product_category`(association table)<br>

`store_product` uses many-to-many relationship and is connected to `store_category` on **product_category**
`store_category` uses recursive (many-to-one relationship to itself) for **parent**<br>

Table Structures:

**store_category:** uses mptt library TreeForeignKey so it automatically generates some necessary fields 
for easy access to objects. 

Manually generated fields are:

| id | category_name | category_description | parent     |
|----|---------------|----------------------|------------|
| 1  | _name_        | _description_        | _category_ |


**store_product:**

| id | product_name | product_description | product_image | product_price | product_quantity |
|----|--------------|---------------------|---------------|---------------|------------------|
| 1  | _name_       | _description_       | _image_       | _price_       | _number_         |


**store_product_product_category:**

| id | product_id   | category_id   |
|----|--------------|---------------|
| 1  | _product_id_ | _category_id_ |


For testing purposes there are 23 products, 19 categories records in the database <3


## **Components** ##
* **store** - This app contains the models(Product and Category) and 3 views for the store.
* **media** - All user uploaded images go to the media folder.
* **store/static** - for static files: CSS
* **templates** - 3 HTML templates for rendering are stored here.
* **db.sqlite3** - Database file.


## **Features** ##
* **Category** - Can be accessed at `/` or `/category/` Displays the 6 root categories and its products count with links to each category page. 
* **Category Products Page** - Can be accessed at `/category/{category_id}/products`. Displays all the products in that category or in its subcategories with statistics about the category and total sum of the product price including its quantity. Uses **Pagination** and Only 6 products are displayed in one page with their prices and images and each product is linked to its detail page. 
  * Statistics are displayed based on the provided tasks which are:
    * The price of the most expensive product in the category
    * The price of the cheapest product in the category
    * The average price of the products
    * The Total sum of all the products prices including its quantities.
* **Product Detail Page** - Can be accessed `/category/{category_id}/products/{product_id}` and Displays the information about the individual Product such as id, name, description, price, ancestor categories, image and quantity.
* **Admin Panel** - Can be accessed at `/admin/`. Default username: `admin`, password: `admin`.
* **Database** - sqlite3 database is used.

## Dependencies
* **Python 3.X**
* **Django 5.1.1**
* **Pillow 10.4.0**
* **Django-debug-toolbar**
* **Django-mptt**

## Usage
Clone the repository:
```bash
git clone https://github.com/hella753/simple_rendering_with_three_page.git
cd simple_rendering_with_three_page
```
To install the dependencies, use the following command in your terminal:
```bash
pip install -r requirements.txt
```
To run the development server, use the following command in your terminal:
```bash
python manage.py runserver
```
To access the application, open your browser and go to http://127.0.0.1:8000/

