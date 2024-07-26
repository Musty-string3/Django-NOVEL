from django.shortcuts import render
from django.views import View
from django.db.models import Count

from text_app.models import Novel

class TopView(View):
    template_name = 'top.html'
    def get(self, request, *args, **kwargs):
        last_three_novels = (Novel.objects.filter(is_public=True)
                            .annotate(sentence_count=Count('sentence'))
                            .order_by('-created_at')[:3])
        return render(request, self.template_name, {
            "last_three_novels": last_three_novels,
        })