from rest_framework import serializers
from .models import ConsentRecord


class ConsentRecordSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = ConsentRecord
        fields = [
            "id",
            "consent_type",
            "version",
            "agreed",
            "agreed_at",
            "revoked_at",
            "is_active",
            "created_at",
        ]
        read_only_fields = fields

    def get_is_active(self, obj):
        return obj.agreed and obj.revoked_at is None


class ConsentGrantSerializer(serializers.Serializer):
    consent_type = serializers.ChoiceField(
        choices=ConsentRecord.ConsentTypes.choices
    )
    version = serializers.CharField(max_length=30, trim_whitespace=True)

    def validate_version(self, value):
        if not value:
            raise serializers.ValidationError("A consent version is required.")
        return value