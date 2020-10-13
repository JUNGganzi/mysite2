#1 from django.shortcuts import render
# from django.http import Http404
# 1
# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.urls import reverse
# from django.shortcuts import get_object_or_404, render

# 2
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
# Create your views here.
# request 라는 인자(클라이언트에게)를 받고 HttpResponse 를 돌려줌 입력 과 출력  출력전 파일로 뭐할지 고름
# 1
# def index(request):
    #1 return HttpResponse("Hello, world.")

    #2 latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    #3 latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

    # 4
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
#  1       
# def detail(request, question_id):
    # 1
    # return HttpResponse("You're looking at question %s." % question_id)

    # 2
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    # 3
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})

    # 4
class DetailView(generic.DetailView):
    # 1
    # model = Question
    # template_name = 'polls/detail.html'

    # 2
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# 1
# def results(request, question_id):
    # 1
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

    # 2
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})

    # 3
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # 1
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))