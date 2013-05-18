import Image
import urllib2
from facepp import API, File
import os
import flickr_api
from config import *


def flickrSaveInfo(token, secret, username):
    text = '%s\n%s\n%s\n%s'%(flickr_key, flickr_secret, token, secret)
    path = './verifiers/%s.verifier'%username
    f = open(path, 'w')
    f.write(text)
    f.close()
    return True


def flickrLoadInfo(username):
    return './verifiers/%s.verifier'%username

def fOauth(username):
    flickr_api.set_keys(api_key = flickr_key, api_secret = flickr_secret)
    a = flickr_api.auth.AuthHandler.load(flickrLoadInfo(username))
    flickr_api.set_auth_handler(a)


def Oauth():   
    return API(API_KEY, API_SECRET)

face_api = Oauth() 


def get_photo_files(username = 'YahooHack2013') :
    fOauth(username)
    user = flickr_api.Person.findByUserName(username)
    photos = user.getPhotos()
    photo_files = []
    for photo in photos :
        photo_files.append(photo.getPhotoFile())
    return photo_files


def getsmallFace(detect_res, pic_path, border = 10, default_size = (150,150)) :
    x = detect_res['face'][0]['position']['center']['x']
    y = detect_res['face'][0]['position']['center']['y']
    x = detect_res['img_width'] * 0.01 * x
    y = detect_res['img_height'] * 0.01 * y
    
    width = detect_res['face'][0]['position']['width'] * detect_res['img_width'] * 0.01
    height = detect_res['face'][0]['position']['height'] * detect_res['img_height'] * 0.01
    
    x1 = int(x-width/2) - border
    y1 = int(y-height/2) - border
    
    x2 = int(x+width/2) + border
    y2 = int(y+width/2) + border
    
    box = (x1,y1,x2,y2)
    
    #Download picture file from flickr
    filename = pic_path[pic_path.rfind('/')+1:]
    if not os.path.isfile(filename):
        req = urllib2.Request(pic_path)
        response = urllib2.urlopen(req)
        pic = response.read()
        f = file(filename,'w')
        f.write(pic)
        f.close()
        
    im = Image.open(filename)
    xim = im.crop(box)
    p = xim.resize(default_size)
    # save as XXXX.(picture format)
    path = './static/avatars/'+detect_res['face'][0]['face_id'] + pic_path[pic_path.rfind('.'):]
    p.save(path)

def cut_faces(photo_files = []) :
    if len(photo_files) <= 0 : return []
    face_ids = []
    for f in photo_files :
        res = face_api.detection.detect(url = f)
        if len(res['face']) == 0 :
            continue
        face_ids.append('/static/avatars/'+res['face'][0]['face_id'] + f[f.rfind('.'):])
        getsmallFace(res,f)
    return face_ids 


def add_faces_to_person (username = 'YahooHack2013', face_id_list = [], defaultGroupName = 'yahoohack', defaultFaceSetName = 'yahoohack_faceset') :
    person = face_api.person.create(person_name = username, group_name = defaultGroupName)
    person_id = person['person_id']
    if len(face_id_list) <= 0 :
        print 'Warning,face_id_list empty'
        return
    face_ids_str = ','.join(face_id_list)
    res_person_add_face = face_api.person.add_face(person_id = person_id, face_id = face_ids_str)
    res_faceset_add_face = face_api.faceset.add_face(faceset_name = defaultFaceSetName, face_id = face_ids_str)
    
    if not res_person_add_face.get('success',False) or not res_faceset_add_face.get('success',False) :
        return False
    return True

def train(defaultGroupName = 'yahoohack', defaultFaceSetName = 'yahoohack_faceset') :
    # asynchronous
    identify_session_id = face_api.train.identify(group_name = defaultGroupName)
    search_session_id = face_api.train.search(faceset_name = defaultFaceSetName)
    return identify_session_id, search_session_id

def get_Train_Result(identify_session_id, search_session_id) :
    identify_res = face_api.info.get_session(session_id = identify_session_id)
    search_res = face_api.info.get_session(session_id = search_session_id)
    print 'identify\t%s\t\tsearch\t%s' % (identify_res['status'], search_res['status'])
    return identify_res['result'], search_res['result']
