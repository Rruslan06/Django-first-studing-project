from django.contrib import admin
from .models import Question, Choice

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 #Три пустых дополнительных поля

class QuestionAdmin(admin.ModelAdmin):
    fieldsets= [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]

    #Благодаря этому мы регулируем, какие колонки отображаются на странице со всеми вопросами
    list_display = ["question_text", "pub_date", "was_published_recently"]

    #Благодаря inlines можно встраивать одни модели в другие для удобства заполнения
    inlines = [ChoiceInline]

    list_filter = ["pub_date"]

    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)

