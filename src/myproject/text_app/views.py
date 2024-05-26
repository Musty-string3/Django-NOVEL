from django.shortcuts import render
from django.views import View
from .models import *

class IndexNovel(View):
    template_name = 'novel/index.html'
    def get(self, request, *args, **kwargs):
        # TODO filterで公開非公開
        novels = NOVEL.objects.all()
        return render(request, self.template_name,{
            "novels": novels,
        })