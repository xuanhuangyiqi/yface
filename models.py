import json
import time
import tornado.database
from config import DATABASE 


class Model:
    def __init__(self):
        self.db = tornado.database.Connection(**DATABASE)

    def create_profile(self, token, secret, username, flickr_id):
        sql = "SELECT * FROM profile WHERE username = '%s'"%username
        results = self.db.query(sql)
        if results:
            sql = "UPDATE profile SET token = '%s', secret='%s' WHERE username='%s'"%(token, secret, username)
            self.db.execute(sql)
        else:
            sql = "INSERT INTO profile(token, secret, username, flickr_id) VALUES ('%s','%s', '%s', '%s')"%(token, secret, username, flickr_id)
            self.db.execute(sql)

    def update_profile(self, username, args):
        sql = "UPDATE profile SET %s WHERE username='%s'"%(','.join(["%s='%s'"%(x, args[x]) for x in args]), username)
        self.db.execute(sql)

    def get_profile(self, yid):
        sql = "SELECT * FROM profile WHERE yid = '%s'"%yid
        return self.db.query(sql)

    def get_profile_by_username(self, username):
        sql = "SELECT * FROM profile WHERE username = '%s'"%username
        return self.db.query(sql)
    def create_record(self, yid, be_yid, ctime, geo):
        sql = "INSERT INTO record(yid, be_yid, ctime, geo) VALUES('%s', '%s', %d, '%s')"%(yid, be_yid, ctime, geo)
        self.db.execute(sql)

    def username2id(self):
        sql = "SELECT * FROM profile"
        p = self.db.query(sql)
        return dict([(x['username'], x['flickr_id']) for x in p])
