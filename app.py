import os
from controller.controller import app


if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0')
