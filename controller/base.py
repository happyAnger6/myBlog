#coding=utf-8
__author__ = 'phithon'
from collections import defaultdict

import pymongo

import tornado.web, json, yaml, os, time, re
from extends.torndsession.sessionhandler import SessionBaseHandler
from util.flash import flash
from util.function import humantime, nl2br
from tornado import gen
from util.function import not_need_login
from util.sendemail import Sendemail

class BaseHandler(SessionBaseHandler):
	def initialize(self):
		self.db = self.settings.get("database")
		self.backend = self.settings.get("thread_pool")
		self.flash = flash(self)
		self.topbar = "home"
		self._current_user = {
				"username": "admin",
				"power": 20,
				"money": 0,
				"login_time": time.time()
			}

	def prepare(self):
		#print("prepare")
		self.add_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-eval'; "
												   "connect-src 'self'; img-src 'self' data:; style-src 'self'; "
												   "font-src 'self'; frame-src 'self'; ")
		self.add_header("X-Frame-Options", "deny")
		self.add_header("X-XSS-Protection", "1; mode=block")
		self.add_header("X-Content-Type-Options", "nosniff")
		self.add_header("x-ua-compatible:", "IE=edge,chrome=1")
		self.clear_header("Server")
		self.power = "guest"
		#print("check_login")
		self.check_login()
		power = {
			0: "user",
			20: "admin"
		}
		if self.current_user and self.current_user.get("power") in power:
			self.power = power[self.current_user["power"]]

		flush = self.get_cookie("flush_info", default=None)#session过期时间已到,需要重新
		if self.current_user and not flush:
			self.flush_session() #将session存储到redis并设置新的current_user
			#print("flush_session")
			self.set_cookie("flush_info", "ok", expires = time.time() + 60 * 10)

	def set_session(self, user):
		try:
			if user["username"] == "guest":
				session = {
				"username": user["username"],
				"power": user["power"],
				"money": user["money"],
				"login_time": time.time()
			}
			else:
				assert ("_id" in user and "username" in user)
				session = {
					"_id": str(user["_id"]),
					"username": user["username"],
					"power": user["power"],
					"money": user["money"],
					"login_time": time.time()
				}
			self.session.set("current_user", session)
			return session
		except:
			return None

	@tornado.web.asynchronous
	@gen.coroutine
	def set_nologin_cookie(self):
		guest="guest"
		user = yield self.db.member.find_one({"username": guest})
		self.guest_current_user = user

	def get_current_user(self):
		#print("get_current_user")
		try:
			user = self.session.get("current_user")#是否是已经合法的session.
			if not user and self.get_cookie("user_info"): #session不合法或者新的或者超时尝试从cookie中获取（注册时记录的remeber me）
				scookie = self.get_secure_cookie("user_info")
				user = json.loads(scookie)
				if not self.set_session(user): #服务端存储本次的session
					assert False
		except:
			user = None
		#print("user1",user)
		if not user:
			#self.set_nologin_cookie()
			user = {
				"username": "guest",
				"power": 0,
				"money": 0,
				"login_time": time.time()
			}
		#print("user",user)
		return user

	def check_login(self):
		#print("check_login 1")
		try:
			assert type(self.current_user) is dict
			assert self.current_user.get('username')
		except AssertionError:
			#print("assertio Error")
			if self.get_cookie("user_info"):
				self.clear_cookie("user_info")
			if self.request.path == "/":
				self.redirect("/public/list/")
			if re.match(r"^/post/([a-f0-9]{24})", self.request.path):
				self.redirect("/public%s" % self.request.path)
			self.custom_error("请先注册或登录", jump="/register")

	@tornado.web.asynchronous
	@gen.coroutine
	def render(self, template_name, **kwargs):
		kwargs["base_url"] = self.settings.get("base_url")
		kwargs["topbar"] = self.topbar
		kwargs["humantime"] = humantime
		kwargs["nl2br"] = nl2br
		kwargs["get_avatar"] = self.get_avatar
		kwargs["get_game_avatar"] = self.get_game_avatar
		kwargs["power"] = self.power
		kwargs["pagenav"] = self.pagenav
		nums = 0
		categorys = []
		try:
			cursor = self.db.category.find({
				'level':"1"
			})
			nums = yield cursor.count()
			categorys = yield cursor.to_list(nums)
			s_2 = []
			cursor_2 = self.db.category.find(
				{
					'level':'2'
				}
			)
			while (yield cursor_2.fetch_next):
				obj = cursor_2.next_object()
				s_2.append((obj['father'],obj['name']))
			sub_categorys = defaultdict(list)
			for k,v in s_2:
				sub_categorys[k].append(v)
			print(sub_categorys)
		except pymongo.errors.DuplicateKeyError as e:
			pass
		kwargs["category_nums"] = nums
		kwargs["categorys"] = categorys
		kwargs["sub_categorys"] = sub_categorys
		#print("render ui",self.ui)
		return super(BaseHandler, self).render(template_name, **kwargs)

	def redirect(self, url, permanent=False, status=None):
		super(BaseHandler, self).redirect(url, permanent, status)
		raise tornado.web.Finish()

	def custom_error(self, info, **kwargs):
		if not self._finished:
			status_code = kwargs.get("status_code", 200)
			self.set_status(status_code)
			error_title = kwargs.get("title", "提示信息")
			error_status = kwargs.get("status", "warning")
			error_jump = kwargs.get("jump", "#back")
			self.render("error.htm", error_info = info, error_status = error_status,
						error_title = error_title, error_jump = error_jump)
		raise tornado.web.Finish()

	def _write_config(self, config):
		with open(self.settings["config_filename"], "w") as f:
			yaml.dump(config, f, default_flow_style = False, default_style = '"')
		for k, v in config["global"].items():
			self.settings[k] = v

	def _read_config(self):
		with open(self.settings["config_filename"], "r") as f:
			config = yaml.load(f)
		return config

	def get_avatar(self, uid):
		static_path = self.settings.get("static_path")
		path = "%s/face/%s/180.png" % (static_path, uid)
		if os.path.exists(path):
			return path
		else:
			return "%s/face/guest.png" % static_path

	def get_game_avatar(self, path):
		static_path = self.settings.get("static_path")
		path = "%s/%s" % (static_path, path)
		#print("path",path)
		if os.path.exists(path):
			return path
		else:
			return "%s/face/guest.png" % static_path

	def get_ipaddress(self):
		if self.settings["intranet"]:
			return self.request.headers.get('X-Real-Ip')
		else:
			return self.request.remote_ip

	def pagenav(self, count, url, each, now,
				pre = '<ul class="am-pagination am-fr admin-content-pagination">', end = '</ul>'):
		_ret = ''
		_pre = pre
		_end = end
		page = (int(count / each) + 1) if (count % each != 0) else (count / each)
		i = now - 5
		while (i <= now + 5) and (i <= page):
			if i > 0:
				if now == i:
					_url = url % i
					_ret += '<li class="am-active"><a class="am-link-muted" href="%s">%d</a></li>' % (_url, i)
				else:
					_url = url % i
					_ret += '<li><a class="am-link-muted" href="%s">%d</a></li>' % (_url, i)
			i += 1
		if now > 6:
			_url = url % 1
			_ret = u'<li><a class="am-link-muted" href="%s">首页</a></li><li class="am-disabled"><a href="#">...</a></li>%s' % (_url, _ret)
		if now + 5 < page:
			_url = url % page
			_ret = u'%s<li class="am-disabled"><a href="#">...</a></li><li><a class="am-link-muted" href="%s">尾页</a></li>' % (_ret, _url)
		if page <= 1:
			_ret = ''
		_ret = _pre + _ret + _end
		return _ret

	@tornado.web.asynchronous
	def flush_session(self):
		def callback(user, error):
			#print("flush_session_callback")
			if not user: return
			user["_id"] = str(user["_id"])
			user["login_time"] = self.current_user["login_time"]
			del user["password"]
			self.session.set("current_user", user)
			self.current_user = user
		self.db.member.find_one({
			"username": self.current_user["username"]
		}, callback = callback)

	@gen.coroutine
	def message(self, touser, content, fromuser = None, jump = None):
		ret = yield self.db.message.insert({
			"from": fromuser,
			"to": touser,
			"content": content,
			"jump": jump,
			"time": time.time(),
			"read": False
		})
		user = yield self.db.member.find_one({
			"username": touser
		})
		if self.settings["email"]["method"] == "mailgun" and "email" in user and user.get("allowemail"):
			Sendemail(self.settings.get("email")).send(
				title=u"来自%s的提醒：%s" % (self.settings["site"]["webname"], content),
				content=u"%s <br /> <a href=\"%s%s\" target=\"_blank\">点击查看</a>"
						% (content, self.settings.get("base_url"), jump),
				to=user["email"]
			)
		raise gen.Return(ret)


class NotFoundHandler(BaseHandler):
	@not_need_login
	def prepare(self):
		BaseHandler.prepare(self)

	def get(self, *args, **kwargs):
		self.set_status(404)
		self.render("404.htm")

	def post(self, *args, **kwargs):
		self.get(*args, **kwargs)