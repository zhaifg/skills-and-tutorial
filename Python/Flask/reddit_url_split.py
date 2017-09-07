import urllib
from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class ListConverter(BaseConverter):
    def __init__(self, url_map, separator="+"):
        super(ListConverter, self).__init__(url_map)
        self.separator = urllib.unique(separator)

    def to_python(self, value):
        return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(BaseConverter.to_url(value) for value in values)

app.url_map.converters['list'] = ListConverter


@app.route('/list1/<list:page_name>/')
def index():
    return 'Separator: {} {}'.format('+', page_name)


@app.route("/list2/<list(separator=u'|'):page_names>/")
def list2(page_names):
    return 'Separator: {} {}'.format('|', page_names)


if __name__ == '__main__':
    app.run(debug=True)
