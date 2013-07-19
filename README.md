flask_blog
==========

A simple blog REST API using Flask.

This service uses virtualenv. To run the service and tests, perform the following steps:

1. git clone https://github.com/JanxSpirit/flask_blog.git
2. cd flask_blog
3. source env/bin/activate
4. To run the service in the included server: python blog.py
5. To run the tests: python test_blog.py

## Resources:

### /posts
###### GET - get a list of all posts
###### POST - add a new blog post
### /posts/post-id
###### GET - get details of a blog post
###### PUT - update details of a blog post
###### DELETE - delete a blog post
### /authors
###### GET - get a list of all authors
### /authors/username
###### GET - get the details of an author
###### PUT - create or update an author with the given username

## Data structures:
### Post
```{
  "title": "A Post Title",
  "author": "validusername",
  "content": "The content of the blog post."
}```

### Author
```
{
  "first_name": "John",
  "last_name": "Does",
  "dob": 2008-04-19
}
```

## Example usage (using httpie)

###### Create an author:
```
http PUT 127.0.0.1:5000/authors/jdoe first_name='John' last_name='Doe' dob='2008-04-19'
HTTP/1.0 201 CREATED
Content-Length: 105
Content-Type: application/json
Date: Fri, 19 Jul 2013 13:27:02 GMT
Location: http://127.0.0.1:5000/authors/jdoe
Server: Werkzeug/0.9.1 Python/2.7.3

{
    "dob": "2008-04-19", 
    "first_name": "John", 
    "last_name": "Doe", 
    "username": "jdoe"
}
```

###### Create a post:
```
http POST 127.0.0.1:5000/posts title='Test Post' author='jdoe' content='Blog Post Content'      
HTTP/1.0 201 CREATED
Content-Length: 140
Content-Type: application/json
Date: Fri, 19 Jul 2013 13:29:31 GMT
Location: http://127.0.0.1:5000/posts/3e7b8d4e-f077-11e2-83e3-00216b2a9376
Server: Werkzeug/0.9.1 Python/2.7.3

{
    "author": "jdoe", 
    "content": "Blog Post Content", 
    "id": "3e7b8d4e-f077-11e2-83e3-00216b2a9376", 
    "title": "Test Post"
}
```

###### List all posts:
```
http GET 127.0.0.1:5000/posts
HTTP/1.0 200 OK
Content-Length: 168
Content-Type: application/json
Date: Fri, 19 Jul 2013 13:30:34 GMT
Server: Werkzeug/0.9.1 Python/2.7.3

[
    {
        "author": "jdoe", 
        "content": "Blog Post Content", 
        "id": "3e7b8d4e-f077-11e2-83e3-00216b2a9376", 
        "title": "Test Post"
    }
]
```

###### List all authors:
```
http GET 127.0.0.1:5000/authors
HTTP/1.0 200 OK
Content-Length: 273
Content-Type: application/json
Date: Fri, 19 Jul 2013 13:31:01 GMT
Server: Werkzeug/0.9.1 Python/2.7.3

[
    {
        "dob": "2008-04-19", 
        "first_name": "John", 
        "last_name": "Doe", 
        "username": "jdoe"
    }
]
```