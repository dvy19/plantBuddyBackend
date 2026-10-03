from celery import shared_task
from django.utils import timezone
from .models import WateringSchedule


@shared_task
def check_watering_schedules():

    now = timezone.localtime()
    current_time = now.time()
    today = now.date()

    schedules = WateringSchedule.objects.filter(
        watering_time__hour=current_time.hour,
        watering_time__minute=current_time.minute,
        next_watering_date=today,
        enabled=True
    )

    for schedule in schedules:

        print(
            f"Water {schedule.plant.name} for user {schedule.user.username}"
        )

        # Send notification here

        schedule.next_watering_date = today + timezone.timedelta(days=2)
        schedule.save()