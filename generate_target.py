import os
import sys
import random as rand
import string
from PIL import Image, ImageDraw, ImageFont

root = "./"

shape_dir = root + "shapes/"
background_dir = root + "backgrounds/"
font_dir = root + "fonts/"

train_dir = root + "../hough_forests_cropped_positive_100_pos_100_neg/"

NUM_TEST_IMAGES = 1000

def main():
    if len(sys.argv) is not 3:
        print "Usage: python generate_test_image.py shape_file out_dir"
        exit(1)

    shapefile = sys.argv[1]
    out_dir   = sys.argv[2]

    shapename = os.path.basename(shapefile).split('.')[0]

    print "%d 1" % NUM_TEST_IMAGES
    for i in range(NUM_TEST_IMAGES):
        image,l = make_image(shapefile)

        fname = shapename + "%03d.png" % i
        image.save(os.path.join(out_dir,fname)
        print "pos%03d.png %d %d %d %d %d %d" % (i, l[0], l[1], l[2], l[3],
                l[2] - l[0], l[3] - l[1])




def make_image(rand_shape):

    _ , shape_name = os.path.split(rand_shape)
    shape_name = shape_name.split('.')[0]

    shape_img = Image.open(rand_shape)
    shape_img.convert("RGBA")
    shape_img = shape_img.rotate(rand.randint(0,20))

    bg_img = Image.open(get_random_file(background_dir))
    bg_img.convert("RGBA")

    shape_img = colorize(shape_img)
    shape_img = resize(shape_img)
    shape_img = add_random_letter(shape_img)
    shape_img = shape_img.rotate(rand.randint(0,360))

    shape = get_random_background(bg_img, shape_img)

    return shape,shape.getbbox()


def get_random_file(path):
    return path + rand.choice(os.listdir(path))


# find all the white pixels in the image and convert them to a random color
def colorize(img):
    color = (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255), 255)
    clear = (255,255,255,0)

    data = img.getdata()
    newdata = []

    for pix in data:
        if pix[0] == 255 and pix[1] == 255 and pix[2] == 255 and pix[3] > 200:
            newdata.append(color)
        else:
            newdata.append(clear)

    img.putdata(newdata)

    return img


# resize shape to some random plausible size
def resize(img):
    size = rand.randint(10,30)
    size = (size,size)
    img.thumbnail(size, Image.ANTIALIAS)

    return img

# place shape somewhere in background such that shape is entirely
# on background (won't dangle off edge)
def get_random_background(background, shape):
    bg_w, bg_h = background.size
    sh_w, sh_h = shape.size

    x_pt = rand.randint(5,bg_w - sh_w-5)
    y_pt = rand.randint(5,bg_h - sh_h-5)

    # pil needs paste "crop box" in form (left, upper, right, lower)
    # mask=shape required to preserve transparency
    background.paste(shape, (x_pt, y_pt, x_pt+sh_w, y_pt + sh_h), mask=shape)

    cropped = background.crop((x_pt-5, y_pt-5, x_pt+sh_w+5, y_pt + sh_h+5))

    return cropped

def add_random_letter(img):
    letter = rand.choice(string.uppercase + string.digits)
    font_name = get_random_file(font_dir)

    img_w,img_h = img.size

    ideal_height = float(img_h)*0.5
    fontsize = 12

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_name, fontsize)

    w,h = draw.textsize(letter, font=font)

    while h > ideal_height:
        fontsize = fontsize - 1
        font = ImageFont.truetype(font_name, fontsize)
        w,h = draw.textsize(letter, font=font)

    while h < ideal_height:
        fontsize = fontsize + 1
        font = ImageFont.truetype(font_name, fontsize)
        w,h = draw.textsize(letter, font=font)



    x_pt = (img_w/2) - (w/2)
    y_pt = (img_h/2) - (h/2)


    color = (rand.randint(0,255), rand.randint(0,255), rand.randint(0,255))
    draw.text((x_pt, y_pt), letter, color, font=font)

    return img


# make a bigger shape, then put and outline around it
def outline(img, color):

    w,h = img.size

    new_h = h + 20
    new_w = w + 20

    bigger = Image.new("RGBA", (new_w, new_h), (255,255,255,0))
    bigger.paste(img, (10, 10, w+10, w+10), mask=img)

    for y in range(new_h):
        for x in range(5):
            bigger.putpixel((x,y),color)
            bigger.putpixel((new_w-1-x,y),color)

    for x in range(new_w):
        for y in range(5):
            bigger.putpixel((x,y),color)
            bigger.putpixel((x,new_h-1-y),color)

    return bigger



if __name__ == "__main__":
    main()
