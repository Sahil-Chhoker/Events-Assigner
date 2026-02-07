from rest_framework import serializers
from .models import Event, Photographer, Assignment


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'email', 'phone', 'is_active']


class AssignmentSerializer(serializers.ModelSerializer):
    photographer = PhotographerSerializer(read_only=True)
    photographer_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Assignment
        fields = ['id', 'event', 'photographer', 'photographer_id']


class EventSerializer(serializers.ModelSerializer):
    assigned_photographers = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'event_name',
            'event_date',
            'photographers_required',
            'created_at',
            'assigned_photographers'
        ]
        read_only_fields = ['created_at']

    def get_assigned_photographers(self, obj):
        assignments = obj.assignments.select_related('photographer').all()
        return PhotographerSerializer(
            [assignment.photographer for assignment in assignments],
            many=True
        ).data


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'event_name',
            'event_date',
            'photographers_required',
            'created_at'
        ]


class PhotographerScheduleSerializer(serializers.ModelSerializer):
    assigned_events = serializers.SerializerMethodField()

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'email', 'phone', 'is_active', 'assigned_events']

    def get_assigned_events(self, obj):
        assignments = obj.assignments.select_related('event').all()
        return EventListSerializer(
            [assignment.event for assignment in assignments],
            many=True
        ).data
