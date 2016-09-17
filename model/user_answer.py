#coding=utf-8
__author__ = 'phithon'
from model.base import BaseModel
try:
	type(u"a") is unicode
except:
	# PY3
	unicode = str

class UserAnswerModel(BaseModel):
	__table__ = "user_answer"
	__invalid__ = {
		"username": {
			"_name": "用户名",
			"_need": True,
			"type": unicode,
			"max_length": 36,
			"min_length": 1,
			"pattern": ur"^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$"
		},
		"index": {
			"_name": "当前题目",
			"type": int,
			"min": -1
		},
		"flag": {
			"_name": "标志",
			"type": int,
			"min": 0
		}
	}
	__msg__ = {
		"type": "%s类型错误",
		"max_length": "%s长度太长",
		"min_length": "%s长度太短",
		"max": "%s过大",
		"min": "%s过小",
		"email": "%s格式错误",
		"number": "%s必须是数字",
		"url": "%s格式错误",
		"pattern": "%s格式错误"
	}
	error_msg = ""