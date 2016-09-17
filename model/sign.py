__author__ = 'zhangxa'
#coding=utf-8

from model.base import BaseModel
from datetime  import date

try:
	type(u"a") is unicode
except:
	# PY3
	unicode = str

class SignModel(BaseModel):
	__table__ = "sign"
	__invalid__ = {
		"username": {
			"_name": "用户名称",
			"_need": True,
			"type": unicode,
			"max_length": 256,
			"min_length": 1
		},
		"sign_year": {
			"_name": "签到年份",
			"type": int
		},
		"sign_month": {
			"_name": "签到月份",
			"type": int
		},
		"sign_day": {
			"_name": "签到日",
			"type": int
		},
        "sign_type":{
            "_name":"签到类型",
            "type":int,
        },
		"remark": {
			"_name": "备注",
			"type": unicode,
			"max_length": 100,
			"min_length": 0
		}
	}
	__msg__ = {
		"type": "%s类型错误",
		"max_length": "%s长度太长",
		"min_length": "%s长度太短",
		"max": "%s过大",
		"min": "%s过小",
	}
	error_msg = ""