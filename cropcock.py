import Image
import pytesseract
# rangle = (int(717*0.75)+20+18+3, int(601*0.7)+30,int(717*0.75)+100,int(601*0.7)+50)#one word 19 :10 other 30
# path="/home/lhn/Desktop/hh/1"
# img = Image.open(str(path) + ".png")
# jpg = img.crop(rangle)
# jpg.save(str(path) + ".jpg")
# jpgzoom = Image.open(str(path) + ".jpg")
# (x, y) = jpgzoom.size
# x_s = 59*4
# y_s = 20*4
# out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
# out.save(path + 'zoom.jpg', 'jpeg', quality=95)
# image = Image.open(str(path) + "zoom.jpg")
# code = pytesseract.image_to_string(image)
# print code
# # if code:
# #     index.append(code)
path = "/home/lhn/Desktop/tmp/"
for i in range(60):
    jpgzoom = Image.open(str(path) + "crop/" + str(i) + ".jpg")
    (x, y) = jpgzoom.size
    x_s = 59 * 4
    y_s = 20 * 4
    out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(path + "zoom/" + str(i) + 'zoom.jpg', 'jpeg', quality=95)
    image = Image.open(str(path) + "zoom/" + str(i) + "zoom.jpg")
    code = pytesseract.image_to_string(image)
    print i
    print code
