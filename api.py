from config.py import flickr_key


def flickrSaveInfo(token, secret):
    text = '''<?xml version="1.0" encoding="utf-8" ?>
    <rsp stat="ok">
    <method>flickr.test.echo</method>
    <api_key>%s</api_key>
    <oauth_token>%s</oauth_token>
    <oauth_verifier>%s</oauth_verifier>
    </rsp>'''%(flickr_key, token, secret)
    path = './xmls/%s.xml'%token
    f = open(path, 'w')
    f.close()
    return True


def flickrLoadInfo(token):
    return './xmls/%s.xml'%token
