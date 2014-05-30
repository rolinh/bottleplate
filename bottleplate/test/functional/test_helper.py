import sys

sys.path = ['../../..'] + sys.path

import bottleplate


def get_app():
    return bottleplate.Bottleplate(template_path='../../app/views/').app
