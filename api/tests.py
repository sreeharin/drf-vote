import sys
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Actor
from api.serializers import ActorSerializer


def create_actor(name='Dummy Actor') -> Actor:
    '''Helper function for creating new actor'''
    return Actor.objects.create(name=name)

def actor_detail(actor_id: int) -> str:
    '''Returns the url for a specific actor'''
    return reverse('api:actor-detail', args=[actor_id])

ENDPOINT_URL = reverse('api:actor-list')


class ApiTestsForSuperUser(TestCase):
    '''Testing APIs which is only accessible by super users'''
    def setUp(self) -> None:
        self.client = APIClient()
        super_user = User.objects.create_superuser(username='admin')
        self.client.force_authenticate(super_user)

    def test_create_new_actor_by_superuser(self) -> None:
        '''Test for creating new actor only by superuser'''
        payload = {'name': 'Dummy Actor'}
        res = self.client.post(ENDPOINT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Actor.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_delete_actor_by_superuser(self) -> None:
        '''Test for deleting actor by superuser'''
        actor = create_actor()
        url = actor_detail(actor.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Actor.objects.filter(name=actor.name).exists()
        self.assertFalse(exists)


class ApiTestForUser(TestCase):
    '''Testing APIs which can be accessed by normal users'''
    def setUp(self) -> None:
        self.client = APIClient()
        user = User.objects.create_user(username='test_user')
        self.client.force_authenticate(user)

    def test_create_actor_by_user(self) -> None:
        '''Testing creating actor by user yields error'''
        payload = {'name': 'Dummy Actor'}
        res = self.client.post(ENDPOINT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        exists = Actor.objects.filter(name=payload['name']).exists()
        self.assertFalse(exists)

    def test_delete_actor_by_user(self) -> None:
        '''Testing deleting actor by user yields error'''
        actor = create_actor()
        url = actor_detail(actor.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        exists = Actor.objects.filter(name=actor.name).exists()
        self.assertTrue(exists)

    def test_upvote_actor_by_authenticated_users(self) -> None:
        '''Test for upvoting actor by authenticated users'''
        actor = create_actor()
        self.assertEqual(actor.vote, 0)
        url = reverse('api:actor-upvote', args=[actor.id])
        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actor.refresh_from_db()
        self.assertEqual(actor.vote, 1)

    def test_downvote_actor_by_authenticated_users(self) -> None:
        '''Test for downvoting actor by authenticated users'''
        actor = create_actor()
        self.assertEqual(actor.vote, 0)
        url = reverse('api:actor-downvote', args=[actor.id])
        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actor.refresh_from_db()
        self.assertEqual(actor.vote, -1)


class ApiTestPublic(TestCase):
    '''Testing APIs which is accessible to the public'''
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_actor_by_anonymous_user(self) -> None:
        '''Testing creating actor by anonymous user yields error'''
        payload = {'name': 'Dummy Actor'}
        res = self.client.post(ENDPOINT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        exists = Actor.objects.filter(name=payload['name']).exists()
        self.assertFalse(exists)

    def test_delete_actor_by_anonymous_user(self) -> None:
        '''Testing deleting actor by anonymous user yields error'''
        actor = create_actor()
        url = actor_detail(actor.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        exists = Actor.objects.filter(name=actor.name).exists()
        self.assertTrue(exists)

    def test_upvote_actor_by_anonymous_user(self) -> None:
        '''Testing upvoting actor by anonymous user yields error'''
        actor = create_actor()
        self.assertEqual(actor.vote, 0)
        url = reverse('api:actor-upvote', args=[actor.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        actor.refresh_from_db()
        self.assertEqual(actor.vote, 0)

    def test_downvote_actor_by_anonymous_user(self) -> None:
        '''Testing downvoting actor by anonymous user yields error'''
        actor = create_actor()
        self.assertEqual(actor.vote, 0)
        url = reverse('api:actor-downvote', args=[actor.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        actor.refresh_from_db()
        self.assertEqual(actor.vote, 0)

    def test_list_actors_by_vote(self) -> None:
        '''Test list actors by the votes they recieved'''
        actor_1 = create_actor(name='Actor 1')
        actor_2 = create_actor(name='Actor 2')
        actor_3 = create_actor(name='Actor 3')
        actor_2.upvote()
        actor_2.upvote()
        actor_3.upvote()
        res = self.client.get(reverse('api:actor-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actors_serializers = ActorSerializer(res.data, many=True)
        self.assertEqual(len(actors_serializers.data), 3)
        self.assertEqual(actors_serializers.data[0]['id'], actor_2.id)
        self.assertEqual(actors_serializers.data[1]['id'], actor_3.id)
        self.assertEqual(actors_serializers.data[2]['id'], actor_1.id)