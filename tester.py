
import cStringIO
#
# CAROUSEL_IMAGE_SPECS = [{'image_name': 'lg',
#                          'size': 'original'},
#                         {'image_name': 'sm',
#                          'size': [400, 400]}]
#
# jpeg_image_buffer = cStringIO.StringIO()
#
#
#
# image_file = Image.open("C:\\Users\\ricks\\Desktop\\jay_pics\\DSCF0397.JPG")
#
# # image_file.show()  # THIS WORKS
#
# image_file.save(jpeg_image_buffer, format='jpeg')
# imgStr = b64encode(jpeg_image_buffer.getvalue())
#
#
#
# file_path = 'C:\\Users\\ricks\\Desktop\\Uploads'
#
# this = UploadImage(image=imgStr, upload_path=file_path, image_specs=CAROUSEL_IMAGE_SPECS, encoding='base64')
#
# error, msg = this.resize_and_save_image()
#
# print out

"""
image_file = Image.open("C:\\Users\\ricks\\Desktop\\jay_pics\\DSCF0397.JPG")

# image_file.show()  # THIS WORKS

image_file.save(jpeg_image_buffer, format='jpeg')
imgStr = b64encode(jpeg_image_buffer.getvalue())

print len(imgStr)

decoded_data = b64decode(imgStr)

file_like = cStringIO.StringIO(decoded_data)

img = Image.open(file_like)
img.show()

img.save('C:\\Users\\ricks\\Desktop\\jay_pics\\foo.jpg')

"""

'''
with open("path/to/file.png", "rb") as f:
    data = f.read()
    print data.encode("base64")

'''


'''

def imagetopy(image, output_file):
    with open(image, 'rb') as fin:
        image_data = fin.read()

    with open(output_file, 'w') as fout:
        fout.write('image_data = '+ repr(image_data))

def pytoimage(pyfile):
    pymodule = __import__(pyfile)
    img = PIL.Image.open(cStringIO.StringIO(pymodule.image_data))
    img.show()



import cStringIO

jpeg_image_buffer = cStringIO.StringIO()
image.save(jpeg_image_buffer, format="JPEG")
imgStr = base64.b64encode(jpeg_image_buffer.getvalue())


'''


'''
with open("yourfile.ext", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())


import cStringIO
import PIL.Image

# assume data contains your decoded image
file_like = cStringIO.StringIO(data)

img = PIL.Image.open(file_like)
img.show()


'''