__author__ = 'zhangxa'

import tornado.ioloop
import tornado.web
import tornado.options

tornado.options.define("port", default=8765, help="Run server on a specific port", type=int)
tornado.options.define("host", default="localhost", help="Run server on a specific host")
tornado.options.define("url", default=None, help="Url to show in HTML")
tornado.options.define("config", default="./config.yaml", help="config file's full path")
tornado.options.parse_command_line()

if not tornado.options.options.url:
	tornado.options.options.url = "http://%s:%d" % (tornado.options.options.host, tornado.options.options.port)

settings = {
	"base_url": tornado.options.options.url,
    "template_path": "templates",
    "static_path": "static",
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

def make_app():
    return tornado.web.Application([
        (r"/",MainHandler)
    ],**settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()