from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create(user=request.user)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=int(choice_id))
        submission.choices.add(choice)

    return show_exam_result(request, submission.id)

def show_exam_result(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    score = 0
    total = 0

    for choice in choices:
        total += 1
        if choice.is_correct:
            score += 1

    context = {
        'score': score,
        'total': total,
        'choices': choices
    }

    return render(request, 'exam_result.html', context)
