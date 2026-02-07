from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from .models import Event, Photographer, Assignment


class PhotographerModelTest(TestCase):
    def setUp(self):
        self.photographer = Photographer.objects.create(
            name='Test Photographer',
            email='test@example.com',
            phone='+1234567890',
            is_active=True
        )

    def test_photographer_creation(self):
        self.assertEqual(self.photographer.name, 'Test Photographer')
        self.assertEqual(self.photographer.email, 'test@example.com')
        self.assertTrue(self.photographer.is_active)

    def test_photographer_str(self):
        self.assertEqual(str(self.photographer), 'Test Photographer')


class EventModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=2
        )

    def test_event_creation(self):
        self.assertEqual(self.event.event_name, 'Test Event')
        self.assertEqual(self.event.photographers_required, 2)

    def test_event_str(self):
        expected = f"Test Event on {self.event.event_date}"
        self.assertEqual(str(self.event), expected)


class AssignmentModelTest(TestCase):
    def setUp(self):
        self.photographer = Photographer.objects.create(
            name='Test Photographer',
            email='test@example.com',
            phone='+1234567890'
        )
        self.event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=1
        )
        self.assignment = Assignment.objects.create(
            event=self.event,
            photographer=self.photographer
        )

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.event, self.event)
        self.assertEqual(self.assignment.photographer, self.photographer)

    def test_assignment_unique_constraint(self):
        with self.assertRaises(Exception):
            Assignment.objects.create(
                event=self.event,
                photographer=self.photographer
            )


class PhotographerAPITest(APITestCase):
    def setUp(self):
        self.photographer_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'is_active': True
        }

    def test_create_photographer(self):
        response = self.client.post(
            reverse('photographer-list'),
            self.photographer_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photographer.objects.count(), 1)
        self.assertEqual(Photographer.objects.get().name, 'John Doe')

    def test_list_photographers(self):
        Photographer.objects.create(**self.photographer_data)
        response = self.client.get(reverse('photographer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_photographer_detail(self):
        photographer = Photographer.objects.create(**self.photographer_data)
        response = self.client.get(
            reverse('photographer-detail', args=[photographer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_update_photographer(self):
        photographer = Photographer.objects.create(**self.photographer_data)
        updated_data = self.photographer_data.copy()
        updated_data['name'] = 'Jane Doe'
        response = self.client.put(
            reverse('photographer-detail', args=[photographer.id]),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        photographer.refresh_from_db()
        self.assertEqual(photographer.name, 'Jane Doe')

    def test_delete_photographer(self):
        photographer = Photographer.objects.create(**self.photographer_data)
        response = self.client.delete(
            reverse('photographer-detail', args=[photographer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photographer.objects.count(), 0)

    def test_photographer_schedule(self):
        photographer = Photographer.objects.create(**self.photographer_data)
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=1
        )
        Assignment.objects.create(event=event, photographer=photographer)
        
        response = self.client.get(
            reverse('photographer-schedule', args=[photographer.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_events']), 1)


class EventAPITest(APITestCase):
    def setUp(self):
        self.event_data = {
            'event_name': 'Corporate Event',
            'event_date': (date.today() + timedelta(days=30)).isoformat(),
            'photographers_required': 2
        }

    def test_create_event(self):
        response = self.client.post(
            reverse('event-list'),
            self.event_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().event_name, 'Corporate Event')

    def test_list_events(self):
        Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=2
        )
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_event_detail(self):
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=2
        )
        response = self.client.get(reverse('event-detail', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event_name'], 'Test Event')

    def test_update_event(self):
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=2
        )
        updated_data = {
            'event_name': 'Updated Event',
            'event_date': (date.today() + timedelta(days=20)).isoformat(),
            'photographers_required': 3
        }
        response = self.client.put(
            reverse('event-detail', args=[event.id]),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.event_name, 'Updated Event')

    def test_delete_event(self):
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=2
        )
        response = self.client.delete(reverse('event-detail', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_get_event_assignments(self):
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=1
        )
        photographer = Photographer.objects.create(
            name='Test Photographer',
            email='test@example.com',
            phone='+1234567890'
        )
        Assignment.objects.create(event=event, photographer=photographer)
        
        response = self.client.get(
            reverse('event-assignments', args=[event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AssignmentLogicTest(APITestCase):
    def setUp(self):
        self.photographer1 = Photographer.objects.create(
            name='Photographer 1',
            email='photo1@example.com',
            phone='+1111111111',
            is_active=True
        )
        self.photographer2 = Photographer.objects.create(
            name='Photographer 2',
            email='photo2@example.com',
            phone='+2222222222',
            is_active=True
        )
        self.photographer3 = Photographer.objects.create(
            name='Photographer 3',
            email='photo3@example.com',
            phone='+3333333333',
            is_active=False
        )
        self.event = Event.objects.create(
            event_name='Wedding',
            event_date=date.today() + timedelta(days=30),
            photographers_required=2
        )

    def test_successful_assignment(self):
        response = self.client.post(
            reverse('event-assign-photographers', args=[self.event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 2)
        self.assertIn('message', response.data)
        self.assertEqual(len(response.data['assigned_photographers']), 2)

    def test_assignment_excludes_inactive_photographers(self):
        response = self.client.post(
            reverse('event-assign-photographers', args=[self.event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assigned_ids = [p['id'] for p in response.data['assigned_photographers']]
        self.assertNotIn(self.photographer3.id, assigned_ids)

    def test_insufficient_photographers(self):
        event = Event.objects.create(
            event_name='Large Event',
            event_date=date.today() + timedelta(days=40),
            photographers_required=5
        )
        response = self.client.post(
            reverse('event-assign-photographers', args=[event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['required'], 5)
        self.assertEqual(response.data['available'], 2)

    def test_past_event_assignment(self):
        past_event = Event.objects.create(
            event_name='Past Event',
            event_date=date.today() - timedelta(days=10),
            photographers_required=1
        )
        response = self.client.post(
            reverse('event-assign-photographers', args=[past_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot assign photographers to past events', response.data['error'])

    def test_already_assigned_event(self):
        Assignment.objects.create(event=self.event, photographer=self.photographer1)
        response = self.client.post(
            reverse('event-assign-photographers', args=[self.event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already assigned', response.data['error'])
        self.assertEqual(response.data['assigned_count'], 1)

    def test_invalid_photographers_required(self):
        invalid_event = Event.objects.create(
            event_name='Invalid Event',
            event_date=date.today() + timedelta(days=20),
            photographers_required=1
        )
        invalid_event.photographers_required = 0
        invalid_event.save()
        
        response = self.client.post(
            reverse('event-assign-photographers', args=[invalid_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_date_conflict_prevention(self):
        event_date = date.today() + timedelta(days=50)
        event1 = Event.objects.create(
            event_name='Event 1',
            event_date=event_date,
            photographers_required=1
        )
        event2 = Event.objects.create(
            event_name='Event 2',
            event_date=event_date,
            photographers_required=1
        )
        
        response1 = self.client.post(
            reverse('event-assign-photographers', args=[event1.id])
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        response2 = self.client.post(
            reverse('event-assign-photographers', args=[event2.id])
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        assigned_to_event1 = set(
            Assignment.objects.filter(event=event1).values_list('photographer_id', flat=True)
        )
        assigned_to_event2 = set(
            Assignment.objects.filter(event=event2).values_list('photographer_id', flat=True)
        )
        
        self.assertEqual(len(assigned_to_event1.intersection(assigned_to_event2)), 0)

    def test_exact_number_of_photographers_assigned(self):
        response = self.client.post(
            reverse('event-assign-photographers', args=[self.event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Assignment.objects.filter(event=self.event).count(),
            self.event.photographers_required
        )


class EdgeCaseTest(APITestCase):
    def test_create_photographer_duplicate_email(self):
        Photographer.objects.create(
            name='Test User',
            email='test@example.com',
            phone='+1234567890'
        )
        response = self.client.post(
            reverse('photographer-list'),
            {
                'name': 'Another User',
                'email': 'test@example.com',
                'phone': '+9876543210'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_event_with_assigned_photographers_in_detail(self):
        event = Event.objects.create(
            event_name='Test Event',
            event_date=date.today() + timedelta(days=10),
            photographers_required=1
        )
        photographer = Photographer.objects.create(
            name='Test Photographer',
            email='test@example.com',
            phone='+1234567890'
        )
        Assignment.objects.create(event=event, photographer=photographer)
        
        response = self.client.get(reverse('event-detail', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_photographers']), 1)
        self.assertEqual(
            response.data['assigned_photographers'][0]['name'],
            'Test Photographer'
        )