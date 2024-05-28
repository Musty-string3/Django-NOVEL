from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .models import *
from .forms import *

class NovelIndexView(View):
    template_name = 'novel/index.html'

    def get(self, request, *args, **kwargs):
        # TODO filterで公開非公開
        novels = Novel.objects.all()
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
            return redirect('text_app:detail_novel', pk=novel.pk)
        messages.error(request, '小説の作成に失敗しました')
        return render(request, self.template_name, {
            'form': form,
        })



class NovelDetailView(View):
    template_name = 'novel/detail.html'

    def get(self, request, pk, *args, **kwargs):
        try:
            novel = Novel.objects.get(id=pk)
        except Novel.DoesNotExist:
            messages.error(request, '指定された小説は存在しません。')
            return redirect('text_app:index_novel')
        return render(request, self.template_name, {
            "novel": novel,
        })

    def post(self, request, pk, *args, **kwargs):
        return redirect('text_app:detail_novel')


class NovelEditView(View):
    template_name = 'novel/edit.html'
    def get_novel_or_redirect(self, pk):
        try:
            return Novel.objects.get(pk=pk)
        except Novel.DoesNotExist:
            messages.error(self.request, '指定された小説は存在しません')
            return redirect('text_app:index_novel')

    def get(self, request, pk, *args, **kwargs):
        novel = self.get_novel_or_redirect(pk)
        form = NovelForm(instance=novel)
        return render(request, self.template_name, {
            'form': form,
            'novel': novel,
        })

    def post(self, request, pk, *args, **kwargs):
        novel = self.get_novel_or_redirect(pk)
        form = NovelForm(request.POST, instance=novel)
        if form.is_valid():
            form.save()
            messages.success(request, '小説の編集に成功しました')
            return redirect('text_app:detail_novel', pk=pk)
        messages.error(request, '小説の編集に失敗しました')
        return render(request, self.template_name, {
            'form': form,
            'novel': novel,
        })

class NovelDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            novel = Novel.objects.get(pk=pk)
            novel.delete()
            messages.info(request, '小説の削除に成功しました')
        except Novel.DoesNotExist:
            messages.error(request, '小説の削除に失敗しました')
            return redirect('text_app:detail_novel', pk=pk)
        return redirect('text_app:index_novel')