import os

# PORT = None
# URI = None
DEBUG = True

# print(os.environ['environment'])
# if os.environ['environment'] != 'production':
#     import src.config_local as config_local
#     PORT = config_local.PORT
#     URI = config_local.URI
#
# else:
import src.config_server as config_server
PORT = config_server.PORT
# URI = config_server.URI