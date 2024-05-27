from django.shortcuts import render
from django.views import View

class TopView(View):
    template_name = 'top.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            
        })