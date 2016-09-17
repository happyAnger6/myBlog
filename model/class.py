#coding=utf-8
__author__ = 'phithon'
from model.base import BaseModel
try:
	type(u"a") is unicode
except:
	# PY3
	unicode = str

class ClassModel(BaseModel):
	__table__ = "class"
	__invalid__ = {
		"classname": {
			"_name": "班级名称",
			"_need": True,
			"type": unicode,
			"max_length": 100,
			"min_length": 1,
			"pattern": ur"^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$"
		},
		"scale": {
			"_name": "班级规模",
			"type": int,
			"min": 0,
			"max":30
		},
		"cur_counts": {
			"_name": "当前人数",
			"type": int,
			"max": 30,
			"min": 0
		},
		"desc": {
			"_name": "班级说明",
			"type": unicode,
			"max_length": 256,
		},
		"members": {
			"_name": "学生列表",
			"type": list,
			"max_length": 100
		},
		"headmaster": {
			"_name": "班主任",
			"type": unicode,
			"max_length": 256
		},
		"monitor": {
			"_name": "班长",
			"type": unicode,
			"max_length": 256,
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