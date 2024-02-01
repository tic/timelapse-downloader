import os
import cv2
from sys import argv

def get_output_name(name = 'output', duplicate = 0):
  fname = name if duplicate == 0 else f'{name} ({duplicate})'
  if not os.path.isfile(f'{fname}.avi'):
    return f'{fname}.avi'

  return get_output_name(name, duplicate + 1)

def get_args():
  argc = len(argv)
  unknown_args_exception = Exception('expected one or two args (input directory, output file name)')
  if argc == 1: # no arguments -- invalid
    raise unknown_args_exception
  elif argc == 2: # one arg -- input directory
    return (argv[1], get_output_name())
  elif argc == 3: # two args -- input directory and output file name
    return (argv[1], get_output_name(argv[2]))
  else: # unknown config -- throw error
    raise unknown_args_exception


def get_bright_images(folder: str, threshold=50, announce_labels=False):
  for file in sorted(os.listdir(folder)):
    filepath = os.path.join(folder, file)
    if os.path.isdir(filepath):
      continue
    
    image = cv2.imread(filepath)
    row_means = image.mean(axis=1)
    sample_mean = row_means[200] # this is from the middle of the image, the last part to get dark
    flattened_pixel = round(sample_mean.mean())

    if announce_labels:
      label = 'night' if flattened_pixel < 50 else 'day'
      print(file, label)

    if flattened_pixel > threshold:
      yield image

def main():
  fps = 30
  resolution = (854, 480)
  image_directory, output_file = get_args()

  vwriter = cv2.VideoWriter(output_file, 0, fps, resolution)

  nwritten = 0
  try:
    for bright_image in get_bright_images(image_directory, announce_labels=False):
      vwriter.write(bright_image)
      nwritten += 1
      print(f'{nwritten} frames written')
  except KeyboardInterrupt:
    pass
  finally:
    cv2.destroyAllWindows()
    vwriter.release()
  
  print('writing complete')

if __name__ == '__main__':
  main()
