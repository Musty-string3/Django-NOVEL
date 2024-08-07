from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.db.models import Count
from django.http import JsonResponse

from .models import *
from .forms import *

class NovelIndexView(View):
    template_name = 'novel/index.html'

    def get(self, request, *args, **kwargs):
        # TODO filterで公開非公開
        novels = Novel.objects.annotate(
            characters_count = Count('sentence__speaker', distinct=True),
            sentences_count = Count('sentence', distinct=True),
        )
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
        sentence_form = SentenceForm()
        character_form = CharacterForm()
        try:
            novel = Novel.objects.get(id=pk)
        except Novel.DoesNotExist:
            messages.error(request, '指定された小説は存在しません。')
            return redirect('text_app:index_novel')

        novel_edit_form = NovelForm(instance=novel)
        sentences = Sentence.objects.filter(novel=novel).prefetch_related('speaker')
        return render(request, self.template_name, {
            "sentence_form":   sentence_form,
            "character_form":  character_form,
            "novel_edit_form": novel_edit_form,
            "novel":           novel,
            "sentences":       sentences,
        })

    def post(self, request, pk, *args, **kwargs):
        sentence_form = SentenceForm(request.POST)
        character_form = CharacterForm(request.POST)
        try:
            novel = Novel.objects.get(pk=pk)
        except Novel.DoesNotExist:
            messages.error(request, '指定された小説は存在しません。')
            return redirect('text_app:detail_novel', pk=pk)

        if sentence_form.is_valid() and character_form.is_valid():
            print(f'リクエスト：{request}')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                """Ajax非同期処理を実行"""
                print('非同期処理を実行します。')
                sentence = sentence_form.save(commit=False)
                sentence.novel = novel
                sentence.save()
                character = character_form.cleaned_data['character']
                sentence.speaker.add(character)
                sentence.save()
                return JsonResponse({
                    'success': True,
                    'speaker_name': character.name,
                    'speaker_icon': character.icon.url,
                    'sentence_text': sentence.text,
                })
        else:
            print('失敗')
            errors = {
                'sentence_form_errors': sentence_form.errors,
                'character_form_errors': character_form.errors,
            }
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': '非同期処理に失敗しました。'
            })

        messages.error(request, '小説の保存に失敗しました。')
        return render(request, self.template_name, {
            'sentence_form': sentence_form,
            'character_form': character_form,
            'novel': novel,
        })


class NovelEditView(View):
    def get_novel_or_redirect(self, pk):
        try:
            return Novel.objects.get(pk=pk)
        except Novel.DoesNotExist:
            messages.error(self.request, '指定された小説は存在しません')
            return redirect('text_app:index_novel')

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


# Character

class CharacterIndexView(View):
    template_name = 'character/index.html'
    def get(self, request, *args, **kwargs):

        characters = Character.objects.all()
        forms = [(character, CharacterCreateForm(instance=character)) for character in characters]
        form = CharacterCreateForm()
        return render(request, self.template_name, {
            'forms': forms,
            'form': form,
        })


class CharacterNewView(View):
    def get(self, request, *args, **kwargs):
        messages.info(request, '何もありませんよ？')
        return redirect('text_app:index_character')

    def post(self, request, *args, **kwargs):
        form = CharacterCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'キャラクターを作成しました')
        else:
            messages.error(request, 'キャラクターの作成に失敗しました')
        return redirect('text_app:index_character')


class CharacterEditView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            messages.error(request, '指定されたキャラクターは存在しません')
            return redirect('text_app:index_character')

        form = CharacterCreateForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            messages.success(request, 'キャラクターの編集を行いました')
            return redirect('text_app:index_character')
        messages.error(request, 'キャラクターの編集ができませんでした')
        return redirect('text_app:index_character')


class CharacterDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            character = Character.objects.get(pk=pk)
            character.delete()
            messages.info(request, 'キャラクター{}の削除をしました。'.format(character.name))
        except Character.DoesNotExist:
            messages.error(request, '指定されたキャラクターは存在しません')
            return redirect('text_app:index_character')

        return redirect('text_app:index_character')


class SentenceEditView(View):
    template_name = 'novel/detail.html'
    def get_sentence_object(self, pk):
        try:
            return Sentence.objects.get(pk=pk)
        except Sentence.DoesNotExist:
            messages.error(self.request, "指定された文章は存在しません")
            return False

    def get(self, request, pk, *args, **kwargs):
        sentence = self.get_sentence_object(pk)
        if not sentence:
            return redirect("text_app:index_novel", pk=pk)

        sentence_edit_form = SentenceForm(instance=sentence)
        character = sentence.speaker.first()
        character_edit_form = CharacterForm()
        novel_edit_form = NovelForm(instance=sentence.novel)
        novel = Novel.objects.get(id=sentence.novel.id)
        sentences = Sentence.objects.filter(novel=novel).prefetch_related('speaker')

        return render(request, self.template_name, {
            "sentence":       sentence,
            "sentence_form":  sentence_edit_form,
            "character_form": character_edit_form,
            "novel_edit_form":     novel_edit_form,
            "novel":               novel,
            "sentences":           sentences,
        })

    def post(self, request, pk, *args, **kwargs):
        sentence = self.get_sentence_object(pk)

        sentence_form = SentenceForm(request.POST, instance=sentence)
        character_form = CharacterForm(request.POST)
        novel = sentence.novel
        print(f'リクエスト：{request}')
        if sentence_form.is_valid() and character_form.is_valid():
            sentence = sentence_form.save(commit=False)
            sentence.novel = novel
            sentence.save()
            character = character_form.cleaned_data['character']
            # TODO: 編集時に新しくデータが作成されるので直す
            if character not in sentence.speaker.all():
                sentence.speaker.add(character)
            sentence.save()
            messages.info(request, "文章の編集を行いました。")
            return redirect('text_app:detail_novel', pk=sentence.novel.id)


class SentenceDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            sentence = Sentence.objects.get(pk=pk)
            sentence.delete()
        except Sentence.DoesNotExist:
            messages(request, "指定された文章は存在しません")
            return redirect('text_app:detail_novel', pk=sentence.novel.id)

        messages.info(request, "文章を削除しました。")
        return redirect('text_app:detail_novel', pk=sentence.novel.id)



class GreetView(View):
    template_name = 'Ajax/index.html'
    greet_form = GreetForm()

    def get(self, request, *args, **kwargs):
        greet_form = GreetForm()
        return render(request, self.template_name, {
            "greet_form": greet_form,
        })

    def post(self, request, *args, **kwargs):
        form = GreetForm(request.POST)
        print(f'リクエスト：{request}')
        if form.is_valid():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                """Ajax非同期処理を実行"""
                print('非同期処理を実行します。')
                name = self.ajax_response(form)
                return JsonResponse({'success': True, 'name': name, 'message': '非同期処理に成功しました。'})
        else:
            print('失敗')
            return JsonResponse({'success': False, 'errors': form.errors, 'message': '非同期処理に失敗しました。'})
        return redirect('text_app:greet')


    def ajax_response(self, form):
        """jQueryに対してレスポンスを返すメソッド"""
        name = form.cleaned_data.get("name")
        return name
