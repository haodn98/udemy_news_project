from django.shortcuts import render, redirect

from answers.models import Answer


# Create your views here.
def answers_list(request):
    answers = Answer.objects.all()
    return render(request, 'back/answers_list.html', {"answers": answers})


def answer_del(request, pk):
    answers_to_del = Answer.objects.get(pk=pk)
    answers_to_del.delete()
    return redirect("answers_list")
