#coding: utf-8
import time
import tornado.web
from config import SITE,static_path
from models import *
from api import *
import json


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return Model()

    @property
    def flickr(self):
        token = self.get_argue
        

class ProfileCreateHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        token = self.get_argument('token')
        secret = self.get_argument('secret')
        username = self.get_argument('username')
        flickr_id = self.get_argument('flickr_id')
        self.db.create_profile(token,secret, username, flickr_id) #insert a user profile
        flickrSaveInfo(token, secret, username)
        
        self.write('ok')

    
'''
    input: yid and about_id
    output: list of head images
'''        
class ProfileUpdateHandler(BaseHandler):
    def post(self):
        # about.me
        username = self.get_argument('username')
        about_id = self.get_argument('about_id')
        args = {"about_id":about_id}
        self.db.update_profile(username, args) #update the "about_id" given yid

        photo_list = get_photo_files(username) # get avatars given yid
        print photo_list
        avatar_list = cut_faces(photo_list)
        result = {'images':avatar_list}
        message = json.dumps(result)
        self.write(message)
        #self.write('ok')


'''
    input: the imgids the user choose
    output: true
'''
class ChooseSelfHandler(BaseHandler):
    def post(self):
        # post photos to face++
        # retrieve & save faces
        # response faces
        token = self.get_argument('token')
        photos = json.loads(self.get_argument('photos'))
        avatar_list = flickrPhotos(token, photos)
        faceppTrainAvatars(yid, avatar_list)
        result = {'result':True}
        message = json.dumps(result)
        self.write(message)


'''
    input: yid, img
    output: {"candidates":[{"be_yid":"xiaomeng","avatar":"http://fdfd"},{"be_yid":"xianyu","avatar":"http://fdfd"}]}
'''
class SearchHandler(BaseHandler):
    def get(self):
        # post photo to face++
        # response a set of faces 
        pass
    def post(self):
        token = self.get_argument('token')
        img = self.request.files['picture'][0]
        img_url = flickrUpload(img)
        be_token_list = faceppDetectFaces(img_url)
        result = {'candidates':be_token_list}
        message = json.dumps(result)
        self.write(message)
    

class ChooseSearchHandler(BaseHandler):
    def post(self):
        # post photo to flickr
        # add be-photographed person
        # add comment?
        token = self.get_argument('token')
        ctime = self.get_argument('ctime')
        geo = self.get_argument('geo')
        be_token = self.getargument('be_token')
        db.create_record(token, be_token, ctime, geo)
        #TODO Flickr_AT
        self.write(json.dumps({'result':True}))
        
