from flask import Flask, request, make_response, url_for
from flask.ext.restful import Resource, Api
from datetime import datetime
import json
import uuid

app = Flask(__name__)
api = Api(app)

posts = {}
authors = {}

class PostList(Resource):
    def get(self):
        return [post for post in posts.values()]

    def post(self):
        if (not validatePost(request.json)):
            return({'msg': 'invalid post content'}, 400)
        if (not request.json.has_key('author') or not authorExists(request.json['author'])):
            return({'msg': 'a valid author must be provided'}, 400)
        id = str(uuid.uuid1())
        addPostIdAndSave(request.json, id)
        return (posts[id], 201, {'Location': ('/posts/%s' % id)})

class PostDetails(Resource):
    def get(self, id):
        if(posts.haskey(id)):
            return posts(id)
        else:
            return ({'msg': 'post id %s not found' % id}, 404)

    def put(self, id):
        if (not validatePost(request.json)):
            return({'msg': 'invalid post content'}, 400)
        if (not request.json.has_key('author') or not authorExists(request.json['author'])):
            return({'msg': 'a valid author must be provided'}, 400)
        if (not posts.has_key(id)):
            return({'msg': 'post id %s not found' % id}, 404)
        addPostIdAndSave(request.json, id)
        return (posts[id], 200, {'Location': ('/posts/%s' % id)})

    def delete(self, id):
        try:
            posts.pop(id)
            return ({'msg': 'deleted post %s' % id}, 200)
        except:
            return ({'msg': 'post id %s not found' % id}, 404)

class AuthorList(Resource):
    def get(self):
        return [author for author in authors.values()]

class AuthorDetails(Resource):
    def put(self, username):
        if (not validateAuthor(request.json)):
            return({'msg': 'invalid author content'}, 400)
        if (not validateDate(request.json['dob'])):
            return({'msg': 'dob must be in the format YYYY-mm-dd'}, 400)

        update = authors.has_key(username)
        authors[username] = request.json
        resp = request.json
        resp['username'] = username
        if (update):
            code = 200
        else:
            code = 201
        return(resp, code, {'Location': ('/authors/%s' % username)})

    def get(self, username):
       if (authorExists(username)):
           return authors(id)
       else:
           return ({'msg': 'author id %s not found' % id}, 404)

api.add_resource(PostList, '/posts', '/posts/')
api.add_resource(PostDetails, '/posts/<string:id>', '/posts/<string:id>/')
api.add_resource(AuthorList, '/authors', '/authors/')
api.add_resource(AuthorDetails, '/authors/<string:username>', '/authors/<string:username>/')

# Utility functions
def validatePost(json):
    return (json.has_key('title') and 
            json.has_key('author') and 
            json.has_key('content') and
            len(json.keys()) == 3)

def validateAuthor(json):
    return (json.has_key('first_name') and
            json.has_key('last_name') and
            json.has_key('dob') and
            len(json.keys()) == 3)

def validateDate(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return True
    except:
        return False

def authorExists(author):
    return authors.has_key(author) 

def addPostIdAndSave(post, id):
    post['id'] = id
    posts[id] = post

if __name__ == '__main__':
    app.run(debug=True)
