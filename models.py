import json
import time
import tornado.database
from config import DATABASE 


class Model:
    def __init__(self):
        self.db = tornado.database.Connection(**DATABASE)

    def create_profile(self, token, secret):
        sql = "INSERT INTO profile(token, secret) VALUES ('%s','%s')"%(token, secret)
        self.db.execute(sql)

    def update_profile(self, yid, args):
        sql = "UPDATE profile SET %s WHERE yid='%s'"%(','.join(["%s='%s'"%(x, args[x]) for x in args]), yid)
        self.db.execute(sql)

    def get_profile(self, yid):
        sql = "SELECT * FROM profile WHERE yid = '%s'"%yid
        return self.db.query(sql)

    def create_record(self, yid, be_yid, ctime, geo):
        sql = "INSERT INTO record(yid, be_yid, ctime, geo) VALUES('%s', '%s', %d, '%s')"%(yid, be_yid, ctime, geo)
        self.db.execute(sql)
