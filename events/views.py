from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Event, Registration
import json

# View all events
def event_list(request):
    events = Event.objects.all().values("id", "name", "description", "date", "location")
    return JsonResponse(list(events), safe=False)

# View event details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    data = {
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "date": event.date,
        "location": event.location,
    }
    return JsonResponse(data)

# Register for an event
@csrf_exempt
def register_event(request, event_id):
    if request.method == "POST":
        body = json.loads(request.body)
        registration = Registration.objects.create(
            event_id=event_id,
            user_name=body.get("user_name"),
            email=body.get("email"),
        )
        return JsonResponse({"message": "Registration successful", "id": registration.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

def registration_list(request):
    registrations = Registration.objects.all().values(
        "id",
        "user_name",
        "email",
        "event_id",
        "registered_at"
    )

    return JsonResponse(list(registrations), safe=False)


@csrf_exempt
def cancel_registration(request, registration_id):
    if request.method == "DELETE":
        registration = get_object_or_404(
            Registration,
            id=registration_id
        )

        registration.delete()

        return JsonResponse(
            {"message": "Registration cancelled successfully"}
        )

    return JsonResponse(
        {"error": "Invalid request method"},
        status=400
    )