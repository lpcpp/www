#!-*-coding:utf-8-*-
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.http import HttpResponse
from www.settings import VERIFY_CODE_TTF
import logging

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

logger = logging.getLogger('runlog')


def create_verify_code():
    logger.debug('enter create verify code')
    chars = string.letters + string.digits
    size = (120, 30)
    # img_type = "GIF"
    mode = "RGB"
    bg_color = (255, 255, 255)
    fg_color = (0, 0, 255)
    font_size = 18
    font_type = VERIFY_CODE_TTF
    length = 4
    draw_lines = True
    # n_line = (1, 2)
    draw_points = True
    point_chance = 2

    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    def get_chars():
        return random.sample(chars, length)

    def create_lines():
        # line_num = random.randint(*n_line)
        begin = (random.randint(0, size[0]), random.randint(0, size[1]))
        end = (random.randint(0, size[0]), random.randint(0, size[1]))
        draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        chance = min(100, max(0, int(point_chance)))
        # print chance
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        c_chars = get_chars()
        # print c_chars
        strs = ' %s ' % ' '.join(c_chars)
        # print strs
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 3), strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, strs


def verify_code(request):
    print 'enter verify_code'
    mstream = StringIO.StringIO()
    img, code = create_verify_code()
    print code
    img.save(mstream, "GIF")
    request.session['verifycode'] = code

    return HttpResponse(mstream.getvalue(), "image/gif")
