from django.test import TestCase
from core.models import Actor


def create_actor(name='Dummy Actor'):
    '''Helper function for creating an actor'''
    return Actor.objects.create(name=name)

class ModelTests(TestCase):
    def setUp(self):
        self.actor = create_actor()

    def test_create_actor(self):
        '''Test creating an actor'''
        exists = Actor.objects.filter(name=self.actor.name).exists()
        self.assertTrue(exists)

    def test_upvote_actor(self):
        '''Test upvoting an actor'''
        self.assertEqual(self.actor.vote, 0)
        self.actor.upvote()
        self.assertEqual(self.actor.vote, 1)

    def test_downvote_actor(self):
        '''Test downvoting an actor'''
        self.assertEqual(self.actor.vote, 0)
        self.actor.downvote()
        self.assertEqual(self.actor.vote, -1)