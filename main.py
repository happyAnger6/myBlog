__author__ = 'zhangxa'

import sys
from concurrent import futures

import yaml
import motor

import tornado.ioloop
import tornado.web
import tornado.options

import controller.base

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
    "config_filename": tornado.options.options.config,
    "compress_response": True,
	"default_handler_class": controller.base.NotFoundHandler,
	"xsrf_cookies": True,
	"static_path": "static",
	"download": "./download",
	"session": {
		"driver": "redis",
		"driver_settings": {
			"host": "localhost",
			"port": 6379,
			"db": 1
		},
		"force_persistence": False,
		"cache_driver": True,
		"cookie_config": {
			"httponly": True
		},
	},
	"thread_pool": futures.ThreadPoolExecutor(4),
	"debug":True
}

class MainHandler(controller.base.BaseHandler):
    def get(self):
        self.render("main.htm")

def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
        (r"^/category/(.*?)/(.*)", "controller.bootstrap.HomeHandler"),
        (r"^/admin/(.*)", "controller.admin.AdminHandler")
    ],**settings)

def init_settings():
    config = {}
    try:
        with open(settings["config_filename"], "r") as fin:
            config = yaml.load(fin)
        if "session" in config:
            settings["session"]["driver_settings"] = config["session"]
    except Exception as e:
        print("cannot found config.yaml file",e)
        sys.exit(0)

# mongodb connection
# format: mongodb://user:pass@host:port/
# database name: minos

    try:
        client = motor.MotorClient(config["database"]["config"])
        database = client[config["database"]["db"]]
        settings["database"] = database
    except:
        print("cannot connect mongodb, check the config.yaml")
        sys.exit(0)

if __name__ == "__main__":
    init_settings()
    #print(settings)
    app = make_app()
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()