from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from events.models import Event, Photographer, Assignment


class Command(BaseCommand):
    help = 'Creates sample data for testing the API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample photographers...')
        
        photographers_data = [
            {
                'name': 'Alice Smith',
                'email': 'alice@example.com',
                'phone': '+1234567891',
                'is_active': True
            },
            {
                'name': 'Bob Johnson',
                'email': 'bob@example.com',
                'phone': '+1234567892',
                'is_active': True
            },
            {
                'name': 'Carol Williams',
                'email': 'carol@example.com',
                'phone': '+1234567893',
                'is_active': True
            },
            {
                'name': 'David Brown',
                'email': 'david@example.com',
                'phone': '+1234567894',
                'is_active': True
            },
            {
                'name': 'Eve Davis',
                'email': 'eve@example.com',
                'phone': '+1234567895',
                'is_active': False
            }
        ]
        
        photographers = []
        for data in photographers_data:
            photographer, created = Photographer.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            photographers.append(photographer)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created photographer: {photographer.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Photographer already exists: {photographer.name}')
                )
        
        self.stdout.write('Creating sample events...')
        
        today = date.today()
        events_data = [
            {
                'event_name': 'Corporate Conference 2026',
                'event_date': today + timedelta(days=30),
                'photographers_required': 2
            },
            {
                'event_name': 'Wedding Ceremony',
                'event_date': today + timedelta(days=45),
                'photographers_required': 3
            },
            {
                'event_name': 'Birthday Party',
                'event_date': today + timedelta(days=15),
                'photographers_required': 1
            },
            {
                'event_name': 'Product Launch',
                'event_date': today + timedelta(days=60),
                'photographers_required': 2
            }
        ]
        
        for data in events_data:
            event, created = Event.objects.get_or_create(
                event_name=data['event_name'],
                event_date=data['event_date'],
                defaults=data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created event: {event.event_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Event already exists: {event.event_name}')
                )
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(f'Total Photographers: {Photographer.objects.count()}')
        self.stdout.write(f'Total Events: {Event.objects.count()}')
