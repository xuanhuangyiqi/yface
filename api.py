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


def getsmallFace(detect_res, pic_path, border = 10, default_size = (100,100)) :
    x = detect_res['face'][0]['position']['center']['x']
    y = detect_res['face'][0]['position']['center']['y']
    x = detect_res['img_width'] * 0.01 * x
    y = detect_res['img_height'] * 0.01 * y
    
    width = detect_res['face'][0]['position']['width'] * detect_res['img_width'] * 0.01
    height = detect_res['face'][0]['position']['height'] * detect_res['img_width'] * 0.01
    
    x1 = int(x-width/2) - border
    y1 = int(y-height/2) - border
    
    x2 = int(x+width/2) + border
    y2 = int(y+width/2) + border
    
    box = (x1,y1,x2,y2)
    
    #Download picture file from flickr
    req = urllib2.Request(pic_path)
    response = urllib2.urlopen(req)
    pic = response.read()
    filename = pic_path[pic_path.rfind('/')+1:]
    f = file(filename,'w')
    f.write(pic)
    f.close()
    
    im = Image.open(filename)
    xim = im.crop(box)
    xim.resize(default_size)
    # save as XXXX.(picture format)
    xim.save('./statics/avatars/'+detect_res['face'][0]['face_id'] + pic_path[pic_path.rfind('.'):])

def cut_faces(photo_files = []) :
    if len(photo_files) <= 0 : return []
    face_ids = []
    for f in photo_files :
        res = face_api.detection.detect(url = f)
        face_ids.append(res['face'][0]['face_id'])
        getsmallFace(res,f)
    return face_ids 


