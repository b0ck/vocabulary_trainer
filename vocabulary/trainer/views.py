from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
import random
from django.contrib import messages

correct_answers_needed = 3


def _get_lesson_results(lesson):
    correct = lesson.vocabulary_pairs.filter(correct_count__gte=correct_answers_needed)
    incorrect = lesson.vocabulary_pairs.filter(correct_count__lt=correct_answers_needed)
    return correct, incorrect


def _get_lesson_languages(lesson):
    native = None
    foreign = None

    if lesson.vocabulary_pairs:
        native = lesson.vocabulary_pairs.first().native.language
        foreign = lesson.vocabulary_pairs.first().foreign.language
    return native, foreign


def reset_lesson_results(request):
    if request.method == 'POST':
        lesson = Lesson.objects.get(pk=request.POST.get('lesson_id'))
        for pair in lesson.vocabulary_pairs.all():
            pair.correct_count = 0
            pair.save()
    return HttpResponseRedirect(reverse('index'))


def index(request):
    lessons_detailed = []
    lessons = Lesson.objects.all()

    for lesson in lessons:
        correct, incorrect = _get_lesson_results(lesson)
        native, foreign = _get_lesson_languages(lesson)

        lesson_details = {
            'lesson': lesson,
            'done_count': correct.count,
            'all_count': lesson.vocabulary_pairs.count,
            'native_language': native,
            'foreign_language': foreign
            # 'language': _get_lesson_language(lesson)
        }

        lessons_detailed.append(lesson_details)

    return render(request, 'trainer/lessons.html', {'lessons': lessons_detailed})


def evaluate_question(request):
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        pair_id = request.POST.get('pair_id')
        reversex = request.POST.get('reverse')
        question = VocabularyPair.objects.get(pk=pair_id)

        form = VocabularyForm(request.POST)

        correct_answer = question.native.text if reversex else question.foreign.text

        if form.is_valid():
            if form.cleaned_data['vocabulary'] == correct_answer:
                question.correct_count += 1
                messages.success(request, 'Your answer was correct!', extra_tags='alert-success')
            else:
                question.correct_count = 0
                messages.error(request, 'Sorry, but your answer was wrong. (Answer: {})'.format(correct_answer), extra_tags='alert-danger')
            question.save()

        response = HttpResponseRedirect(reverse('lesson_view', args=(lesson_id,)))
        response['Location'] += '?last_pair_id=' + pair_id
        if reversex:
            response['Location'] += '&direction=reverse'
        return response


def show_question(request, lesson_id):
    last_pair_id = request.GET.get('last_pair_id')
    reverse = request.GET.get('direction') == 'reverse'

    lesson = Lesson.objects.get(pk=lesson_id)
    correct, incorrect = _get_lesson_results(lesson)
    pair = random.choice(incorrect) if incorrect else None

    # do not pick the sample question twice if possible
    if last_pair_id and pair and incorrect.count() > 1:
        if str(pair.id) == last_pair_id:
            pair = next(incorrect.iterator())

    form = VocabularyForm()

    context = {
        'lesson': lesson,
        'done_count': correct.count,
        'all_count': lesson.vocabulary_pairs.count,
        'pair': pair,
        'form': form,
        'reverse': reverse
    }

    return render(request, 'trainer/question.html', context)
