
from pymongo import MongoClient
client = MongoClient('127.0.0.1',27017)
db = client.pymo_test
posts = db.posts
post_data = {
    'title': 'this is a test',
    'content': 'pymongo is fun',
    'author': 'kiki'
}
result = posts.insert_one(post_data)
print('one post: %s' % result.inserted_id)


