from datetime import date
from django.db.models import Q, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Photographer, Assignment
from .serializers import (
    EventSerializer,
    EventListSerializer,
    PhotographerSerializer,
    PhotographerScheduleSerializer,
    AssignmentSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer

    @action(detail=True, methods=['post'], url_path='assign-photographers')
    def assign_photographers(self, request, pk=None):
        event = self.get_object()

        if event.photographers_required <= 0:
            return Response(
                {'error': 'Photographers required must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event.event_date < date.today():
            return Response(
                {'error': 'Cannot assign photographers to past events'},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_assignments = Assignment.objects.filter(event=event).count()
        if existing_assignments > 0:
            return Response(
                {
                    'error': 'Photographers already assigned to this event',
                    'assigned_count': existing_assignments
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        assigned_photographer_ids = Assignment.objects.filter(
            event__event_date=event.event_date
        ).values_list('photographer_id', flat=True)

        available_photographers = Photographer.objects.filter(
            is_active=True
        ).exclude(
            id__in=assigned_photographer_ids
        )[:event.photographers_required]

        available_count = available_photographers.count()

        if available_count < event.photographers_required:
            return Response(
                {
                    'error': 'Not enough photographers available',
                    'required': event.photographers_required,
                    'available': available_count
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        assignments = []
        for photographer in available_photographers:
            assignment = Assignment.objects.create(
                event=event,
                photographer=photographer
            )
            assignments.append(assignment)

        assigned_photographers = [
            assignment.photographer for assignment in assignments
        ]

        return Response(
            {
                'message': 'Photographers assigned successfully',
                'event': EventSerializer(event).data,
                'assigned_photographers': PhotographerSerializer(
                    assigned_photographers,
                    many=True
                ).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        event = self.get_object()
        assignments = Assignment.objects.filter(event=event).select_related(
            'photographer'
        )
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        photographer = self.get_object()
        serializer = PhotographerScheduleSerializer(photographer)
        return Response(serializer.data)
