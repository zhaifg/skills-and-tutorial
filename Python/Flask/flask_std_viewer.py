from flask import Flask, request, rend_template
from flask.views import View

app = Flask(__name__, template_folder='../../template')

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return rend_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != 'GET':
            return 'UNSUPPORTED!'
        context = {'users' : self.get_user()}
        return self.render_template(context)

class UserView(BaseView):
    def get_template_name(self):
        return 'chapater3/section1/users.html'

    def get_users(self):
        return [{
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
        }]

app.add_url_rule('/users', view_func=UserView.as_view('userview'))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)

