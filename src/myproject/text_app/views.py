from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import *

class IndexNovelView(View):
    template_name = 'novel/index.html'
    def get(self, request, *args, **kwargs):
        # TODO filterで公開非公開
        novels = NOVEL.objects.all()
        return render(request, self.template_name,{
            "novels": novels,
        })


class DetailNovelView(View):
    template_name = 'novel/detail.html'
    def get(self, request, pk, *args, **kwargs):
        try:
            novel = NOVEL.objects.get(id=pk)
        except (NOVEL.DoesNotExist, Exception):
            messages.error(request, '指定された小説は存在しません。')
            return redirect('text_app:index_novel')
        return render(request, self.template_name, {
            "novel": novel,
        })

    def post(self, request, pk, *args, **kwargs):
        return redirect('text_app:detail_novel')