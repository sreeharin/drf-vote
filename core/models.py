from django.db import models


class Actor(models.Model):
    '''Model for actors'''
    name = models.CharField(max_length=64)
    vote = models.IntegerField(default=0)

    def upvote(self) -> None:
        '''Increment the vote count by 1'''
        self.vote += 1
        self.save()

    def downvote(self) -> None:
        '''Decrement the vote count by 1'''
        self.vote -= 1
        self.save()
