from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import requests
import shutil
import random



def WriteImage(img, name, server):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("ABeeZee-Italic.otf", 50)
    draw.text((588, 133),name,(255,255,255),font=font)
    draw.text((378, 282),server,(255,255,255),font=font)
    return img

def downloader(image_url):
    randinput = "welcomeimg/input_{}.png".format(random.randint(0,1000))
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        with open(randinput, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return randinput

def ImageWrite(imgurl, name, server):
    randinput=downloader(imgurl)
    im = Image.open(randinput)
    im = im.resize((250, 250));
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    background = Image.open('welcomeimg/background.png')
    background.paste(im, (100, 115), im)
    WriteImage(background, name, server)
    randimgname = "welcomeimg/welcome_{}.png".format(random.randint(0,1000))
    background.save(randimgname)
    return [randimgname, randinput]
