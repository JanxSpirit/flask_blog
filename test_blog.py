import blog
import unittest
import json

class BlogTestCase(unittest.TestCase):

    def setUp(self):
        self.app = blog.app.test_client()

    # /authors
    def test_a_empty_authors(self):
        r = self.app.get('/authors')
        assert len(json.loads(r.data)) == 0
        assert r.status_code == 200

    def test_b_add_author(self):
        r = self.app.put('/authors/johndoe', data=json.dumps({
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'dob': '2008-04-19'}), content_type='application/json')
        j = json.loads(r.data)
        assert j.has_key('username')
        assert j.has_key('first_name')
        assert j.has_key('last_name')
        assert j.has_key('dob')
        assert r.status_code == 201

    def test_c_update_author(self):
        r = self.app.put('/authors/johndoe', data=json.dumps({
                    'first_name': 'Johnny',
                    'last_name': 'Doe',
                    'dob': '2008-04-19'}), content_type='application/json')
        j = json.loads(r.data)
        assert j.has_key('username')
        assert j.has_key('first_name')
        assert j.has_key('last_name')
        assert j.has_key('dob')
        assert r.status_code == 200

    def test_d_bad_author(self):
        r = self.app.put('/authors/johndoe', data=json.dumps({
                    'first_name': 'Johnny'}), content_type='application/json')
        assert '{"msg": "invalid author content"}' in r.data
        assert r.status_code == 400

    def test_e_bad_date_format(self):
        r = self.app.put('/authors/johndoe', data=json.dumps({
                    'first_name': 'Johnny',
                    'last_name': 'Doe',
                    'dob': '2008-APRIL-19'}), content_type='application/json')
        assert '{"msg": "dob must be in the format YYYY-mm-dd"}' in r.data
        assert r.status_code == 400

    def test_f_get_authors(self):
        r = self.app.get('/authors')
        j = json.loads(r.data)
        assert len(j) == 1
        assert r.status_code == 200

    # /posts
    def test_g_empty_posts(self):
        r = self.app.get('/posts')
        assert len(json.loads(r.data)) == 0
        assert r.status_code == 200

    def test_h_add_posts(self):
        r = self.app.post('/posts', data=json.dumps({
                                'title':'Test Post',
                                'author':'johndoe',
                                'content':'This is a test post'}), content_type='application/json')
        j = json.loads(r.data)
        assert j.has_key('id')
        assert j.has_key('title')
        assert j.has_key('content')
        assert j.has_key('author')
        assert r.status_code == 201

    def test_i_bad_post(self):
        r = self.app.post('/posts', data=json.dumps({
            'title':'This Post Will Fail'}), content_type='application/json')
        assert '{"msg": "invalid post content"}' in r.data
        assert r.status_code == 400

    def test_j_get_posts(self):
        r = self.app.get('/posts')
        j = json.loads(r.data)
        assert len(j) == 1
        assert r.status_code == 200

    def test_k_update_post(self):
        r = self.app.post('/posts', data=json.dumps({
                    'title':'Test Update Post',
                    'author':'johndoe',
                    'content':'This is a test post to be updated'}), content_type='application/json')
        assert r.status_code == 201
        id = json.loads(r.data)['id']
        ru = self.app.put('/posts/%s' % id, data=json.dumps({
                    'title':'Test Update Post (updated)',
                    'author':'johndoe',
                    'content':'This has been updated'}), content_type='application/json')
        j = json.loads(ru.data)
        assert j.has_key('id')
        assert (j.has_key('title') and j['title'] == u'Test Update Post (updated)')
        assert (j.has_key('content') and j['content'] == u'This has been updated')
        assert j.has_key('author')
        assert ru.status_code == 200

    def test_l_update_bad_post(self):
        r = self.app.post('/posts', data=json.dumps({
                    'title':'Test Update Post Bad',
                    'author':'johndoe',
                    'content':'This is a test post to be updated incorrectly'}), 
                          content_type='application/json')
        assert r.status_code == 201
        id = json.loads(r.data)['id']
        ru = self.app.put('/posts/%s' % id, data=json.dumps({
                    'title':'Test Update Post',
                    'author':'johndoe'}), content_type='application/json')
        assert '{"msg": "invalid post content"}' in ru.data
        assert ru.status_code == 400

    def test_m_update_post_invalid_author(self):
        r = self.app.post('/posts', data=json.dumps({
                    'title':'Test Update Invalid Author',
                    'author':'johndoe',
                    'content':'This is a test post to be updated with a bad author'}), 
                          content_type='application/json')
        assert r.status_code == 201
        id = json.loads(r.data)['id']
        ru = self.app.put('/posts/%s' % id, data=json.dumps({
                    'title':'Test Update Post',
                    'author':'doesnotexist',
                    'content':'This is a test post to be updated with a bad author'}), 
                          content_type='application/json')
        assert '{"msg": "a valid author must be provided"}' in ru.data
        assert ru.status_code == 400

    def test_n_update_post_does_not_exist(self):
         ru = self.app.put('/posts/foo', data=json.dumps({
                     'title':'Test Update Post',
                     'author':'johndoe',
                     'content':'This is a test post to be updated with a bad id'}), 
                           content_type='application/json')
         assert '{"msg": "post id foo not found"}' in ru.data
         assert ru.status_code == 404

    def test_o_delete_post(self):
         r = self.app.post('/posts', data=json.dumps({
                    'title':'Test Delete Post',
                    'author':'johndoe',
                    'content':'This is a test post to1 be deleted'}), 
                          content_type='application/json')
         assert r.status_code == 201
         id = json.loads(r.data)['id']
         rd = self.app.delete('/posts/%s' % id)
         assert '{"msg": "deleted post %s"}' % id in rd.data
         assert rd.status_code == 200

    def test_p_delete_post_does_not_exist(self):
        r = self.app.delete('/posts/foo')
        assert '{"msg": "post id foo not found"}' in r.data
        assert r.status_code == 404

if __name__ == '__main__':
    unittest.main()
