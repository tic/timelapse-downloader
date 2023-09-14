from dropbox import Dropbox
from config import config

dropbox_config = config['dropbox']

def get_client(params: dict) -> Dropbox:
  global access_token
  client = Dropbox(
    oauth2_access_token=access_token,
    app_key=params['app_key'],
    app_secret=params['app_secret'],
    oauth2_refresh_token=params['refresh_token'],
  )

  access_token = client._oauth2_access_token
  return client

def download_files():
  print('[DROPBOX] downloading file past cutoff')
  try:
    client = get_client()
    file_result = client.files_list_folder(dropbox_config['path'], recursive=False, limit=2000)
    for file in file_result.files:
      print(file)

  except Exception as err:
    print(f'[DROPBOX] encountered error: {err}')
