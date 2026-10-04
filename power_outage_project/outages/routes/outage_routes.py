"""URL routes for the outage API."""

from django.urls import path

from outages.controllers import (
    AssignTechnicianView,
    OutageReportDetailView,
    OutageReportListCreateView,
    ProgressUpdateView,
)


urlpatterns = [
    path("reports/", OutageReportListCreateView.as_view(), name="report-list-create"),
    path("reports/<int:pk>/", OutageReportDetailView.as_view(), name="report-detail"),
    path("reports/<int:pk>/assign/", AssignTechnicianView.as_view(), name="report-assign"),
    path("reports/<int:pk>/progress/", ProgressUpdateView.as_view(), name="report-progress"),
]
