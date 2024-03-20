from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from feedback.forms import FeedbackForm
from lyceum.settings import DJANGO_MAIL


def feedback(request):
    templates = "feedback/feedback.html"
    feedback_form = FeedbackForm(request.POST or None)
    if request.method == "POST":
        if feedback_form.is_valid():
            text = feedback_form.cleaned_data.get("text")
            mail = feedback_form.cleaned_data.get("mail")
            send_mail(
                "",
                text,
                f"from{DJANGO_MAIL}",
                [mail],
                fail_silently=False,
            )
            messages.success(request, "Письмо успешно отправлено")
            return redirect(reverse("feedback:feedback"))

    context = {
        "title": "Обратная связь",
        "form": feedback_form,
    }
    return render(request, templates, context)


__all__ = []
