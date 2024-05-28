from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .models import *
from .froms import *

class NovelIndexView(View):
    template_name = 'novel/index.html'
    def get(self, request, *args, **kwargs):
        # TODO filterで公開非公開
        novels = NOVEL.objects.all()
        return render(request, self.template_name,{
            "novels": novels,
        })


class NovelNewView(View):
    template_name = 'novel/new.html'
    def get(self, request, *args, **kwargs):
        form = NovelForm()
        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = NovelForm(request.POST)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.created_by = request.user
            novel.save()
            messages.success(request, '小説を作成しました')
            return redirect('text_app:index_novel')
        messages.error(request, '小説の作成に失敗しました')
        return render(request, self.template_name, {
            'form': form,
        })



class NovelDetailView(View):
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