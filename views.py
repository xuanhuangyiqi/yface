#coding: utf-8
import time
import tornado.web
from config import SITE,static_path
from models import *
import json

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return Model()
        

'''
    input: the yid
    output: the list of head images
'''
def getAvatars(yid):
    # post photos to face++
        # retrieve & save faces
        # response faces
    #call the function from lixin
    pass
    
'''
    input: yid, avatar_list 
'''
def trainAvatars(yid, avatar_list):
    #call the function from lixin
    pass
'''
    return face list
'''
def detectFaces(img):
    pass

class ProfileCreateHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        token = self.get_argument('token')
        secret = self.get_argument('secret')
        self.db.create_profile(token,secret) #insert a user profile
        result = {'result':True}
        message = json.dumps(result)
        self.write(message)


class GetProfileHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        pass
    
'''
    input: yid and about_id
    output: list of head images
'''        
class ProfileUpdateHandler(BaseHandler):
    def post(self):
        # about.me
        token = self.get_argument('token')
        about_id = self.get_argument('about_id')
        facepp_id = faceppCreatePerson()
        args = {"about_id":about_id, "facepp_id":facepp_id}
        db.update_profile(token,args) #update the "about_id" given yid

        photo_list = flickrGetPhotos(token) # get avatars given yid
        avatar_list = faceppGetAvatars(photo_list)
        result = {'images':avatar_list}
        message = json.dumps(result)
        self.write(message)


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
        
