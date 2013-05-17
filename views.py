#coding: utf-8
import time
import tornado.web
from config import SITE,static_path
from models import *
from filters import *

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return Model()
        

class YFeedBackHandler(BaseHandler):
    def get(self):
        # Create Account
        pass


class ProfileUpdateHandler(BaseHandler):
    def get(self):
        # about.me
        pass


class ChooseSelfHandler(BaseHandler):
    def get(self):
        # post photos to face++
        # retrieve & save faces
        # response faces
        pass


class SaveSelfHandler(BaseHandler):
    def get(self):
        pass



class SearchHandler(BaseHandler):
    def get(self):
        # post photo to face++
        # response a set of faces 
        pass


class ChooseSearchHandler(BaseHandler):
    def get(self):
        # post photo to flickr
        # add be-photographed person
        # add comment?
        pass
