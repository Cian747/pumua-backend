
from django.core.management.base import BaseCommand

from practices.models import PracticeCategory


CATEGORIES = [
    {
        "name": "Calm and relaxation",
        "slug": "calm-and-relaxation",
        "description": "Slow, gentle breathing to settle your body.",
        "display_order": 1,
    },
    {
        "name": "Better sleep",
        "slug": "better-sleep",
        "description": "Wind down and prepare for rest.",
        "display_order": 2,
    },
    {
        "name": "Focus and energy",
        "slug": "focus-and-energy",
        "description": "Wake up your mind and improve focus.",
        "display_order": 3,
    },
    {
        "name": "Stress and anxiety relief",
        "slug": "stress-and-anxiety-relief",
        "description": "Release tension in the moment.",
        "display_order": 4,
    },
    {
        "name": "Breath control",
        "slug": "breath-control",
        "description": "Build capacity with structured techniques.",
        "display_order": 5,
    },
]


class Command(BaseCommand):

    help = "Create the default Breath Connection practice categories"

    def handle(self, *args, **options):

        for category in CATEGORIES:
            _, created = PracticeCategory.objects.update_or_create(
                slug=category["slug"],
                defaults=category,
            )

            status = "Created" if created else "Updated"

            self.stdout.write(
                f"{status}: {category['name']}"
            )

        self.stdout.write(
            self.style.SUCCESS("Practice categories seeded.")
        )
