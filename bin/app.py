import sys

sys.path.insert(0, '..')

from lib.web import app  # noqa


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True, port=9000)
