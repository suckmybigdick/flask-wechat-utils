#coding:utf8
from flask import Flask

from flask_wechat_utils import bp as wechat_bp
from flask_wechat_utils import db as wechat_db
from flask_wechat_utils import config as user_config
from flask_wechat_utils.message_template import config as message_template_config

from flask_wechat_utils import api
from flask_wechat_utils.user.utils import auth
from flask_restplus import Resource, fields

#-------------------------------------------
# app
#-------------------------------------------
app = Flask(__name__)

#-------------------------------------------
# config
#-------------------------------------------
app.config['MONGODB_SETTINGS'] = {
	'db': 'xxx',
	'host': 'mongo',
	'port': 27017,
}

user_config.WXAPP_ID = 'xxx'
user_config.WXAPP_SECRET = 'xxx'
user_config.WEB_NAME = 'myweb'
message_template_config.TEMPLATE_ID = None

#-------------------------------------------
# 固定写法，不需要修改，初始化数据库+注册路由
#-------------------------------------------
wechat_db.init_app(app)
app.register_blueprint(wechat_bp)


#-------------------------------------------
# my routees
#-------------------------------------------
ns = api.namespace(
	'myapplication', 
	description='descriptions of my_routes'
)

@ns.route('/my_auth_route')	# http://127.0.0.1:5000/myweb/myapplication/my_auth_route
class AuthRoute(Resource):

	@auth
	def get(self):

		return {
			'code':0,
			'nickname':self.wechat_user.nickname,
			'avatar':self.wechat_user.avatar,
		}

#-------------------------------------------
# 用户写好自己的application的route,model等,然后这里导入路由即可,这里使用该库默认路由
#-------------------------------------------
from flask_wechat_utils.user import routes				#使用默认user路由
from flask_wechat_utils.message_template import routes	#使用默认message_template路由

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)