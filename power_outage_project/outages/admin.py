from django.contrib import admin

from outages.models import Assignment, OutageReport, ProgressUpdate


@admin.register(OutageReport)
class OutageReportAdmin(admin.ModelAdmin):
    list_display = ("id", "area", "customer", "priority", "status", "created_at")
    list_filter = ("status", "priority", "area")
    search_fields = ("area", "description", "customer__username")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("outage_report", "technician", "assigned_by", "status", "assigned_at")
    list_filter = ("status",)


@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ("assignment", "technician", "status", "created_at")
    list_filter = ("status",)
