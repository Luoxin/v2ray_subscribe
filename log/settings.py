import os
import sys
sys.path.append("../")
from conf.conf import LOG_DEBUG, MODEL_NAME, LOG_PATH


LOGCONFIG = {'name': MODEL_NAME, 'debug': LOG_DEBUG, "log_path": LOG_PATH}

# if os.path.exists(LOG_PATH):
#     pass
# else:
#     os.mkdir(LOG_PATH)
