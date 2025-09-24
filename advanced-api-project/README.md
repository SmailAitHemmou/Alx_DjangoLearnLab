# Advanced API Project - Views

This project demonstrates advanced API development using Django REST Framework.

## Endpoints
- `/api/books/`  
  - `GET` : List all books (open to all).
  - `POST` : Create a new book (authenticated users only).

- `/api/books/<id>/`  
  - `GET` : Retrieve details of a single book (open to all).
  - `PUT/PATCH` : Update a book (authenticated users only).
  - `DELETE` : Remove a book (authenticated users only).

## Permissions
- Read access (list/retrieve) is available to all users.
- Write access (create/update/delete) requires authentication.

### Filtering, Searching, and Ordering

- Filter books: `/api/books/?title=BookName&publication_year=2020`
- Search books: `/api/books/?search=keyword`
- Order books: `/api/books/?ordering=publication_year` or `/api/books/?ordering=-publication_year`
