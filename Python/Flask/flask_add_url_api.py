from flask import Flask, jsonify
from flask.views import MethodView

class UserAPI(MethodView):
    def get(self):
        return jsonify({
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
            })

    def post(self):
        return 'UNSOPPORTED!'

app.add_url_rule('/user', view_func=UserAPI.as_view('userview'))
if __name__ == '__main__':
    app.run()
