import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    #Любое название, НО ОБЯЗАТЕЛЬНО ПЕРВОЕ "test_"
    def test_was_published_recently_with_future_question(self):
        """
        Тест должен возвращать False для  вопросов, которые написаны в будущем(pub_date в будущем)
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)



    def test_was_published_recently_with_past_question(self):
        """
        Тест должен возвращать False для  вопросов, которые написаны более дня назад
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)



    def test_was_published_recently_with_recent_question(self):
        """
        Тест должен возвращать True для  вопросов, которые попали в промежуток вчерашнего дня от времени написания
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """Создаем вопрос с переданным текстом и датой(минусовые это прошлое, плюсы - в будущем)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionIndexViewsTest(TestCase):
    def test_no_questions(self):
        """Если вопроса нет, то выводим сообщение"""
        response = self.client.get(reverse("first_app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_past_question(self):
        """Если вопрос в прошлом, нужно его отобразить"""
        question = create_question("Past, question", days=-30)
        response = self.client.get(reverse("first_app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question])

    def test_future_question(self):
        """Если вопрос в будущем, то его отображать не нужно"""
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("first_app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_past_and_future_question(self):
        """Если есть вопрос в прошлом и будущем покажется только в прошлом"""
        create_question(question_text="Future question", days=30)
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("first_app:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"],  [question])

    def test_two_past_questions(self):
        """Если два вопроса в прошлом, то их оба отображаем"""
        question1 = create_question(question_text="First past question", days=-30)
        question2 = create_question(question_text="Second past question", days=-10)
        response = self.client.get(reverse("first_app:index"))
        self.assertQuerySetEqual(response.context["latest_questions_list"], [question2, question1])



class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """Если вопрос ещё не выложен, то страница не откроется и статус должен быть 404"""
        question = create_question(question_text="Future Question", days=1)
        response = self.client.get(reverse("first_app:detail", args=(question.pk,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Если вопрос выложен, то страница должна открыться и содержимое(вопрос) отобразится"""
        question = create_question(question_text="Past Question", days=-1)
        response = self.client.get(reverse("first_app:detail", args=(question.pk,)))
        self.assertContains(response, question.question_text)