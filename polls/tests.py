import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

def create_poll(question, days):
		"""
		Creates poll with given question published the given number of days
		offset to now(negative for polls in past, positive for future polls)
		"""
		return Poll.objects.create(question=question, 
				pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):

	def test_index_view_with_no_polls(self):
		"""
		If no polls exist, display appropriate error message.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls found")
		self.assertQuerysetEqual(response.context["latest_poll_list"], [])

	def test_index_view_with_a_past_poll(self):
		"""
		Polls with past date should be displayed
		"""
		create_poll(question="Past poll.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context["latest_poll_list"],
			["<Poll: Past poll.>"]
		)

	def test_index_view_with_a_future_poll(self):
		"""
		Polls with a future date shouldn't be displayed
		"""
		create_poll(question="Future poll.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_a_future_and_past_poll(self):
		"""
		Past polls should be displayed, future polls shouldn't
		"""
		create_poll(question="Past poll.", days=-30)
		create_poll(question="Future poll.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			["<Poll: Past poll.>"])

	def test_index_view_with_two_past_polls(self):
		"""
		Two polls should be displayed
		"""
		create_poll(question="Past poll 1.", days=-30)
		create_poll(question="Past poll 2.", days=-32)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'],
			["<Poll: Past poll 1.>", "<Poll: Past poll 2.>"]
		)

class PollIndexDetailTests(TestCase):

	def test_detail_view_with_a_future_poll(self):
		"""
		404 should be returned
		"""
		future_poll = create_poll(question="Future poll.", days=30)
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		"""
		Should show the poll
		"""
		past_poll = create_poll(question="Past poll.", days=-30)
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
		self.assertContains(response, past_poll.question, status_code=200)


class PollMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""
		was_published_recently should return False when polls have a future
		pub_date
		"""

		future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_old_poll(self):
		"""
		was_published_recently should return false for polls whose pub_date
		is older than 1 day
		"""
		old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_poll.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		"""
		should return true
		"""
		recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(), True)

