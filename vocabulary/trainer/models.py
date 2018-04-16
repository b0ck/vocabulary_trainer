from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


class Vocabulary(models.Model):
    text = models.CharField(max_length=100)
    note = models.CharField(max_length=100, blank=True)
    transcription = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        note = ' ({}) '.format(self.note) if self.note else ''
        return '({}) {}{}'.format(self.language.code, self.text, note)

    def question_label(self):
        note = ' ({}) '.format(self.note) if self.note else ''
        return '{}{}'.format(self.text, note)


class VocabularyPair(models.Model):
    native = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='pairs_native')
    foreign = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='pairs_foreign')
    correct_count = models.IntegerField(default=0)

    def __str__(self):
        return '{} -> {}'.format(self.native, self.foreign)


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    vocabulary_pairs = models.ManyToManyField(VocabularyPair, blank=True)

    def __str__(self):
        if self.description:
            return '{}: {}'.format(self.name, self.description)
        return self.name
