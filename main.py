import tornado.web
import tornado.ioloop
from views import *
import config



if __name__ == "__main__":
    app = tornado.web.Application([
        ('/profile/create', ProfileCreateHandler),
        ('/prifile/update', ProfileUpdateHandler),
        ],
        static_path=config.static_path)
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
