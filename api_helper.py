#!/usr/bin/env python2
import Image
import urllib2
from facepp import API, File
import os
import flickr_api


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
    xim.save(detect_res['face'][0]['face_id'] + pic_path[pic_path.rfind('.'):])
    
def Oauth(key_file = '', verifier_file = 'flickr.verifier') :   
    API_KEY = '0b9ca8fca8041e791d684c0b88fe5708'
    API_SECRET = '4WlmUalSo3_SLScJyBaaJvgMCWjK3-WR'

    flickr_key = '31573003eefcabb832334323de5027a0'
    flickr_secret = 'f66472f76f1992ee'

    flickr_api.set_keys(api_key = flickr_key, api_secret = flickr_secret)

    a = flickr_api.auth.AuthHandler.load(verifier_file)
    flickr_api.set_auth_handler(a)
    face_api = API(API_KEY, API_SECRET)
    return face_api
 
face_api = Oauth()

def get_photo_files(username = 'YahooHack2013') :
    user = flickr_api.Person.findByUserName(username)
    photos = user.getPhotos()
    photo_files = []
    for photo in photos :
        photo_files.append(photo.getPhotoFile())
    return photo_files

def cut_faces(photo_files = []) :
    if len(photo_files) <= 0 : return []
    face_ids = []
    for f in photo_files :
        res = face_api.detection.detect(url = f)
        face_ids.append(detect_res['face'][0]['face_id'])
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

def face_search(photo_url = '', photo_img = '', defaultFaceSetName = 'yahoohack_faceset') :
    if photo_url == '' and photo_img == '':
        print 'photo is empty!'    
        return
    if photo_img != '' :
        res = face_api.detection.detect(img = File(photo_img))
    if photo_url != '' :
        res = face_api.detection.detect(url = photo_url)
    face_id = res['face'][0]['face_id']
    search_res = face_api.recognition.search(key_face_id = face_id, faceset_name = defaultFaceSetName, count=3)
    faces_res = search_res['candidate']
    print faces_res
    
    
if __name__ == '__main__' :
    Oauth()
    f = open('face_id.list','r')
    face_id_list = f.read().split()
    f.close()
    #print 'add_faces\t', add_faces_to_person(face_id_list = face_id_list)
    
    #print train()
    #photo_files = get_photo_files()
    #cut_faces(photo_files)
    
    face_search(photo_img = '1.jpg')


