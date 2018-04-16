from django.contrib import admin

from .models import *

admin.site.register(Language)
admin.site.register(Vocabulary)
admin.site.register(VocabularyPair)
admin.site.register(Lesson)
