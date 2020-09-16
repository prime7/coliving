from django.db import models


FAQ_CATEGORY = (
    (1,'General'),
    (2,'DUOO'),
)
class Faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    faq_category = models.IntegerField(choices=FAQ_CATEGORY)

    def __str__(self):
        return self.question