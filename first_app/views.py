from django.http import HttpResponse, HttpResponseRedirect #Чтобы перенаправлять пользователя с POST на GET запросы(страницы)
from .models import Question, Choice

from django.utils import timezone

from django.db.models import F #Чтобы работать с полями и не было состояния гонки

from django.http import Http404 # Чтобы вывести страницу 404 (длинный способ)

from django.template import loader #Нужен чтобы использовать шаблоны(длинный путь)
from django.shortcuts import render, get_object_or_404 #Нужен чтобы использовать шаблоны(короткий путь) и ошибку 404

from django.urls import reverse #Как в шаблонах в Питоне используем удобную запись и не хардкордим страницу куда перейти

from django.views import generic #Чтобы использовать базовые представления(Generic View) 
# Create your views here.


#Старый вариант
# def index(request): #Это обязательный параметр - request. Ссылка на специальный класс HttpRequest и содержит информацию о запросе, в частности о сессии, куках
#     latest_questions_list = Question.objects.order_by("-pub_date")[:5]
#     #template = loader.get_template("first_app/index.html") (длинный путь)
#     context = {"latest_questions_list": latest_questions_list }
#     #return HttpResponse(template.render(context, request)) (длинный путь)
#     return render(request, "first_app/index.html", context) #(короткий путь)

#Новый вариант
class IndexView(generic.ListView):
    template_name = "first_app/index.html"
    context_object_name = "latest_questions_list"
    
    def get_queryset(self):
        """Возвращает список из 5 вопросов, кроме тех  которые должны быть опубликованы в будущем"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
 

# Старый вариант
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "first_app/detail.html", {"question": question})


# Новый вариант
class DetailView(generic.DetailView):
    template_name = "first_app/detail.html"
    context_object_name = "question"

    def get_queryset(self):
        """Убираем те, которые ещё не были опубликованы"""
        return Question.objects.filter(pub_date__lte=timezone.now())


# Старый вариант
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "first_app/results.html", {"question": question})


#Новый вариант
class ResultView(generic.DetailView):
    model = Question
    template_name = "first_app/results.html"  


#Здесь HttpResponseRedirect; reverse; F; 
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    
    except (KeyError, Choice.DoesNotExist):
        #Переадрессуемся на эту же страницу с сообщением об ошибке
        return render(
            request, "first_app/detail.html", {
                "question": question,
                "error_message": "Вы не выбрали ни один из вариантов ответа",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("first_app:results", args=(question.id,)))