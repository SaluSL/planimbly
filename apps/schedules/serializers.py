from rest_framework import serializers

from .models import ShiftType, Preference, Absence, Assignment, JobTime, FreeDay
from ..accounts.models import Employee
from ..accounts.serializers import EmployeeSerializer


class JobTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTime
        fields = ['id', 'year', 'january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']


class FreeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeDay
        fields = ['id', 'day', 'name']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ShiftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftType
        fields = ['id', 'hour_start', 'hour_end', 'name', 'workplace', 'demand', 'color', 'active_days', 'is_used']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['id', 'shift_type', 'employee', 'active_days']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate(self, data):
        """Check if user in shift_type workplace"""
        if data['shift_type'].workplace not in data['employee'].user_workplace.all():
            raise serializers.ValidationError("User is not assigned to workplace")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['shift_type_obj'] = ShiftTypeSerializer(ShiftType.objects.get(pk=data['shift_type'])).data
        return data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'shift_type', 'employee', 'start', 'end', 'negative_flag']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['shift_type_obj'] = ShiftTypeSerializer(ShiftType.objects.get(pk=data['shift_type'])).data
        return data


class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['id', 'start', 'end', 'employee', 'type', 'hours_number']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['employee_obj'] = EmployeeSerializer(Employee.objects.get(pk=data['employee'])).data
        return data
