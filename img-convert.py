import argparse
from os import listdir, path, mkdir
from PIL import Image, ImageOps

parser = argparse.ArgumentParser(description='Converts images to JPEG to compresses them.')
parser.add_argument('path', help='A folder or image path.')
parser.add_argument('-q', '--quality', default=75, help='output JPEG quality as a percentage', type=int)
parser.add_argument('-s', '--scale', help='scales the image down to the specified size', type=int)
args = parser.parse_args()

formats = ('.jpg', '.jpeg', '.png', '.bmp')
saved = 0
images = 0


def compressImage(p, q, outputDir=False, s=None):
	global saved, images
	picture = Image.open(p)
	name = path.basename(p)
	if s:
		picture.thumbnail((s, s), Image.ANTIALIAS)

	if not picture.mode == 'RGB':
		picture = picture.convert('RGB')
	picture = ImageOps.exif_transpose(picture)
	if outputDir:
		new_path = path.join(path.dirname(p), 'compressed', path.splitext(name)[0]+'.jpg')
	else:
		new_path = path.join(path.dirname(p), 'compressed_'+path.splitext(name)[0]+'.jpg')
	picture.save(new_path, "JPEG", optimize=True, quality=q)
	picture.close()
	old_size = path.getsize(p)
	new_size = path.getsize(new_path)
	saved += old_size - new_size
	images += 1
	print('compressed '+name+' ('+formatBytes(old_size), '->', formatBytes(new_size)+')')


def formatBytes(b):
	if b > 1073741824:
		return str(round(b/1073741824, 2))+' GB'
	elif b > 1048576:
		return str(round(b/1048576, 2))+' MB'
	elif b > 1024:
		return str(round(b/1024, 2))+' KB'
	else:
		return b+' B'


if path.isdir(args.path):
	if not path.exists(path.join(args.path, 'compressed')):
		mkdir(path.join(args.path, 'compressed'))
	for img in listdir(args.path):
		if path.splitext(img)[1].lower() in formats: # checks file extension
			compressImage(path.join(args.path, img), args.quality, True, args.scale)
	print(images, 'images compressed saving', formatBytes(saved))
elif path.isfile(args.path) and path.splitext(args.path)[1].lower() in formats:
	compressImage(args.path, args.quality, False, args.scale)
else:
	print('Invalid path.')
