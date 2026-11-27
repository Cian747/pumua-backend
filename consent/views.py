from django.db import transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import ConsentRecord
from .serializers import (
    ConsentRecordSerializer,
    ConsentGrantSerializer,
)


class ConsentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = ConsentRecord.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ConsentRecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsentGrantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consent_type = serializer.validated_data["consent_type"]
        version = serializer.validated_data["version"]

        with transaction.atomic():
            active_record = ConsentRecord.objects.filter(
                user=request.user,
                consent_type=consent_type,
                agreed=True,
                revoked_at__isnull=True,
            ).first()

            if active_record:
                return Response(
                    {
                        "detail": "Active consent already exists.",
                        "consent": ConsentRecordSerializer(active_record).data,
                    },
                    status=status.HTTP_200_OK,
                )

            record = ConsentRecord.objects.create(
                user=request.user,
                consent_type=consent_type,
                version=version,
                agreed=True,
                agreed_at=timezone.now(),
            )

        return Response(
            ConsentRecordSerializer(record).data,
            status=status.HTTP_201_CREATED,
        )


class ConsentWithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            record = get_object_or_404(
                ConsentRecord.objects.select_for_update(),
                pk=pk,
                user=request.user,
                agreed=True,
                revoked_at__isnull=True,
            )

            record.revoked_at = timezone.now()
            record.save(update_fields=["revoked_at", "updated_at"])

        return Response(
            {
                "detail": "Consent withdrawn successfully.",
                "consent": ConsentRecordSerializer(record).data,
            },
            status=status.HTTP_200_OK,
        )