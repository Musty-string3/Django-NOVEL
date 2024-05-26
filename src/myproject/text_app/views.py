from django.shortcuts import render
from django.views import View

class IndexNovel(View):
    def get(self, request, *args, **kwargs):
        template_name = 'novel/index.html'
        return render(request, template_name)