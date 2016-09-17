#coding=utf-8
__author__ = 'phithon'
from model.base import BaseModel
try:
	type(u"a") is unicode
except:
	# PY3
	unicode = str

class GameModel(BaseModel):
	__table__ = "games"
	__invalid__ = {
		"name": {
			"_name": "游戏名称",
			"_need": True,
			"type": unicode,
			"max_length": 256,
			"min_length": 1
		},
		"type": {
			"_name": "游戏类型",
			"type": int,
			"min": 0
		},
		"play_type": {
			"_name": "操作类型",
			"type": int,
			"min": 0
		},
		"resource_type": {
			"_name": "资源类型",
			"type": int,
			"min": 0
		},
		"path": {
			"_name": "资源路径",
			"type": unicode,
			"max_length": 255,
			"min_length": 1
		},
		"question": {
			"_name": "游戏问题",
			"_need": True,
			"type": unicode,
			"max_length": 256,
			"min_length": 1
		},
		"answer1": {
			"_name": "答案A",
			"type": unicode,
			"max_length": 100,
			"min_length": 1
		},
		"answer2": {
			"_name": "答案B",
			"type": unicode,
			"max_length": 100,
			"min_length": 1
		},
		"answer3": {
			"_name": "答案C",
			"type": unicode,
			"max_length": 100,
			"min_length": 1
		},
		"answer4": {
			"_name": "答案D",
			"type": unicode,
			"max_length": 100,
			"min_length": 1
		},
		"right_answer": {
			"_name": "正确答案",
			"type": unicode,
			"max_length": 256,
			"min_length": 1
		},
		"switch": {
			"_name": "开关",
			"type": int,
			"max":1,
			"min": 0
		},
		"plays": {
			"_name": "被玩次数",
			"type": int,
			"min": 0
		},
		"right_plays": {
			"_name": "正确次数",
			"type": int,
			"min": 0
		},
		"wrong_plays": {
			"_name": "错误次数",
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
	}
	error_msg = ""