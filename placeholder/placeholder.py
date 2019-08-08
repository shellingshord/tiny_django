import os
import sys

from django.http import HttpResponse
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django import forms

from io import BytesIO
from PIL import Image,ImageDraw

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', 'ph$ec4=hl8t6k-jo3uk@=xv2r-0wafm&t*q$+qei()ohytgjm$')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

settings.configure(
    DEBUG = DEBUG,
    SECRET_KEY = SECRET_KEY,
    ALLOWED_HOSTS = ALLOWED_HOSTS,
    ROOT_URLCONF = __name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)
class ImageForm(forms.Form):
    """docstring for ImageForm"""
    height = forms.IntegerField(min_value=1,max_value=2000)
    width = forms.IntegerField(min_value=1,max_value=2000) 

    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB',(width, height))
        draw = ImageDraw.Draw(image)
        text = '{} x {}'.format(width,height)
        textwidth, textheight = draw.textsize(text)
        if textwidth < width and textheight < height:
            texttop = (height - textheight) // 2
            textleft = (width - textwidth) // 2
            draw.text((textleft, texttop), text, fill=(255,255,255))
        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        return content
        

def placeholder(request, width, height):
    form = ImageForm({'height':height,'width':width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponse('Invalid Image Request')
def index(request):
    return HttpResponse('HELLO DJANGO TINY')

urlpatterns = [
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',placeholder,name='placeholder'),
    url(r'^$',index,name='homepage'),
]

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)