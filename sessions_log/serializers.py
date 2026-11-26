from rest_framework import serializers

from .models import SessionLog, MonthlyGoal


class SessionLogSerializer(serializers.ModelSerializer):
    technique_name = serializers.CharField(source="technique.name",read_only=True)

    class Meta:
        model = SessionLog
        fields = [
            "id",
            "technique",
            "technique_name",
            "duration_seconds",
            "completed_at",
            "completed",
            "created_at",
        ]
        read_only_fields = ["id", "completed", "created_at"]

    def validate_duration_seconds(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Session duration must be greater than zero."
            )
        return value


class MonthlyGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyGoal
        fields = [
            "id",
            "year",
            "month",
            "target_sessions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_month(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError(
                "Month must be between 1 and 12."
            )
        return value

    def validate_target_sessions(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Monthly goal must be at least one session."
            )
        return value
