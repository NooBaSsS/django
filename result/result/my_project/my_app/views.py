from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from django.conf import settings
from .forms import UserForm
from django.core.files.storage import FileSystemStorage
from .analyser import TextAnalyser
from os.path import join, splitext

users = ['a', 'b']

base_dir = settings.BASE_DIR


def index(request):
    context = {
        'users': users
    }
    return render(request, 'my_app/index.html', context)


def add(request):
    if request.method == 'GET':
        form_fields = UserForm()
        context = {
            'form_fields': form_fields,
        }
        return render(request, 'my_app/add.html', context)
    elif request.method == 'POST':
        form_fields = UserForm(request.POST, request.FILES)
        if form_fields.is_valid():
            file = request.FILES['file']
            file_system = FileSystemStorage()
            file_name = file_system.save(file.name, file)
            file_url = file_system.url(file_name)

            source_file = join(settings.MEDIA_ROOT, file_name)
            wc_width = int(request.POST['wc_width'])
            wc_height = int(request.POST['wc_height'])
            pos = request.POST.getlist('pos')
            words_ammount = int(request.POST['wc_words'])
            wc_color = request.POST['color']
            destination_file = join(settings.MEDIA_ROOT, splitext(file.name)[0] + '.png')

            TextAnalyser(
                source_file=source_file,
                destination_file=destination_file,
                parts_of_speech=pos,
                words_ammount=words_ammount,
                wc_width=wc_width,
                wc_height=wc_height,
                wc_background=wc_color,
                wc_margin=10,
            )
            context = {
                'url': destination_file
            }
            return render(request, 'my_app/download.html', context)
        else:
            context = {
                        'form_fields': form_fields,
            }
            return render(request, 'my_app/add.html', context)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'],
                                      content='этот метод не разрешен'
                                      )
