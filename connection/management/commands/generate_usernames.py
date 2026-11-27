from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import transaction


class Command(BaseCommand):
    help = "Generate unique usernames for users who do not have one."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        users = User.objects.filter(
            username__isnull=True
        ).order_by("date_joined", "email")

        updated = 0

        for user in users:
            email_prefix = user.email.split("@")[0]
            base = slugify(email_prefix)[:140] or "member"

            candidate = base
            suffix = 2

            while User.objects.filter(
                username__iexact=candidate
            ).exclude(pk=user.pk).exists():

                candidate = (
                    f"{base[:140 - len(str(suffix))]}{suffix}"
                )
                suffix += 1

            user.username = candidate
            user.save(update_fields=["username"])

            updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated usernames for {updated} users."
            )
        )

        remaining = User.objects.filter(
            username__isnull=True
        ).count()

        self.stdout.write(
            f"Users still missing usernames: {remaining}"
        )
