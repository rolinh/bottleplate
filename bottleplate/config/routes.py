from bottleplate.app.controllers.assets_controller import AssetsController
from bottleplate.app.controllers.index_controller import IndexController


def setup_routing(app):
    # static files
    app.route('/img/<filename>', 'GET', AssetsController.img)
    app.route('/js/<filename>', 'GET', AssetsController.js)
    app.route('/css/<filename>', 'GET', AssetsController.css)
    app.route('/favicon.ico', 'GET', AssetsController.favicon)
    app.route('/favicon.png', 'GET', AssetsController.favicon)

    # home
    app.route('/', 'GET', IndexController().index)
