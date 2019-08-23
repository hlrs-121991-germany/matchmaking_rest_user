from django.contrib import admin
from questions.models import Question, Answer, UserAnswer

class AnswerMemberInline(admin.TabularInline):
    model = Question.answers.through

class AnswerAdmin(admin.ModelAdmin):
    inlines = [
        AnswerMemberInline,
    ]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ AnswerMemberInline ]
    exclude = ('answers',)
#    class Meta:
#        model = Question

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer)

# Register your models here.
