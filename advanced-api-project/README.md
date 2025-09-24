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
