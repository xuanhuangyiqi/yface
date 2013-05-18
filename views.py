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
        username = self.get_argument('username')
        about_id = self.get_argument('about_id')
        args = {"about_id":about_id}
        self.db.update_profile(username, args) #update the "about_id" given yid

        #photo_list = get_photo_files(username) # get avatars given yid
        #avatar_list = cut_faces(photo_list)
        #result = {'images':avatar_list}
        #message = json.dumps(result)
        #print message
        #self.write(message)
        self.write('{"images": ["/static/avatars/153cfc969b96b984caa89d0ac82213be.jpg", "/static/avatars/2f5e7e32f402e22cf27168f067663a79.jpg", "/static/avatars/e8fcb7d2997b1e6e92ae40979053e91b.jpg", "/static/avatars/d24302d8218507b7810c26b18e9b3590.jpg", "/static/avatars/5498054dd74920b2e2c0759080d24984.jpg", "/static/avatars/ba1fed373a321266a8accb8a8475a301.jpg", "/static/avatars/4fd8d9d888560f8744cf51d429a3b5ec.jpg", "/static/avatars/729dfe13e21eaf2fd5edb6f9263e605f.jpg", "/static/avatars/668e94a6a04e3dcebad9cc62e98f6641.jpg", "/static/avatars/d86a3468d2e5c2612caddbeb4fc8cf8a.jpg"]}')


'''
    input: the imgids the user choose
    output: true
'''
class ChooseSelfHandler(BaseHandler):
    def post(self):
        print 'test'
        # post photos to face++
        # retrieve & save faces
        # response faces
        username = self.get_argument('username')
        avatars = [x[x.rfind('/')+1:] for x in json.loads(self.get_argument('avatars'))]
        avatars = [x[:x.find('.')] for x in avatars]
        #avatars = ['153cfc969b96b984caa89d0ac82213be', 'd24302d8218507b7810c26b18e9b3590','d86a3468d2e5c2612caddbeb4fc8cf8a','729dfe13e21eaf2fd5edb6f9263e605f']
        #iid, sid = add_faces_to_person(username, avatars)
        #while True:
        #   get_Train_Result(iid, sid)
        #   import time
        #   time.sleep(1)

        #print iid, sid


        self.write('ok')


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
        print message
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
        
