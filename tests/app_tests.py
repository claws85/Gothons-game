from nose.tools import *
from app import app
from gothonweb.planisphere import *

app.config['TESTING'] = True
web = app.test_client()



def test_index():
    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 200)

    rv = web.get('/game', follow_redirects=True)
    assert_equal(rv.status_code, 200)

    data = {}
    rv = web.get('/game', follow_redirects=True, data=data)
    assert_in(b"Gothons", rv.data)

#    rv = web.get('/hello', follow_redirects=True)
#   assert*_equal(rv.status_code, 200)
#    assert*_in(b"Fill Out This Form", rv.data)

#    data = {'name': 'Zed', 'greet': 'Hola'}
#    rv = web.post('/hello', follow_redirects=True, data=data)
#    assert_*in(b"Zed", rv.data)
#    assert_*in(b"Hola", rv.data)