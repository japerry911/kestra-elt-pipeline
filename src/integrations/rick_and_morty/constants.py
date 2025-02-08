from datetime import datetime

import pytz

RUN_DATETIME = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
