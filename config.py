from dotenv import load_dotenv
from os import getenv as os_getenv
from json import loads as json_loads

def getenv(key: str, default='', alert_if_missing=False, json=False):
  rval = default
  value = os_getenv(key)
  if value is None:
    if alert_if_missing:
      print(f'[CONFIG] tried to access env variable "{key}" but it was not found')
  else:
    rval = value

  return json_loads(rval) if json else rval

load_dotenv()

config = {
  'dropbox': getenv('TDL_DROPBOX_CONFIG', '{}', json=True)
}
