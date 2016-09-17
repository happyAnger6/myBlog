__author__ = 'zhangxa'

import tornado
from controller.base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self,*args,**kwargs):
        print(args)
        self.render("%s/%s.html"%(args[0],args[1]))