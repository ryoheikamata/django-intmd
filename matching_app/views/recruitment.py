import structlog

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from matching_app.forms.recruitment import RecruitmentForm
from matching_app.models import Recruitment

RECRUITMENT_TIMELINE_PAGE_SIZE = 10

logger = structlog.get_logger(__name__)

@login_required
@require_http_methods(["GET"])
def recruitment_timeline(request: HttpRequest) -> HttpResponse:
    recruitments = Recruitment.objects.select_related("user").all()
    pagenator = Paginator(recruitments, RECRUITMENT_TIMELINE_PAGE_SIZE)
    page_number = request.GET.get("page", default=1)
    page_obj = pagenator.page(page_number)

    return render(
        request,
        "recruitment_timeline.html",
        {"page_obj": page_obj},
    )

@login_required
@require_http_methods(["GET"])
def recruitment_detail(request: HttpRequest, pk: int) -> HttpResponse:
    recruitment = get_object_or_404(Recruitment.objects.select_related("user"), pk=pk)
    return render(request, "recruitment_detail.html", {"recruitment": recruitment})

@login_required
@require_http_methods(["GET", "POST"])
def recruitment_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RecruitmentForm(request.POST)
        if form.is_valid():
            recruitment = form.save(commit=False)
            recruitment.user = request.user
            recruitment.save()
            return redirect("recruitment_timeline")
        else:
            logger.error("Invalid create recruitment form", error=form.errors)
    else:
        form = RecruitmentForm()

    return render(
        request,
        "recruitment_create.html",
        {"form": form},
    )