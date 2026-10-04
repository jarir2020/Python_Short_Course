"""HTTP controllers for outage reports, assignments, and progress."""

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.exceptions import WorkflowError
from common.permissions import IsAdminRole, IsCustomerRole, IsTechnicianRole
from outages.repositories import get_report
from outages.serializers import (
    AdminOutageUpdateSerializer,
    AssignTechnicianSerializer,
    OutageReportCreateSerializer,
    OutageReportReadSerializer,
    ProgressUpdateCreateSerializer,
    ProgressUpdateReadSerializer,
)
from outages.services import (
    add_technician_progress,
    assign_technician,
    create_customer_report,
    get_visible_report,
    list_visible_reports,
    update_report_by_admin,
)


def _visible_or_404(user, report_id):
    report = get_visible_report(user, report_id)
    if report is None:
        raise NotFound("Outage report not found.")
    return report


class OutageReportListCreateView(APIView):
    def get(self, request):
        reports = list_visible_reports(request.user)
        return Response(OutageReportReadSerializer(reports, many=True).data)

    def post(self, request):
        serializer = OutageReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = create_customer_report(request.user, serializer.validated_data)
        return Response(
            OutageReportReadSerializer(report).data,
            status=status.HTTP_201_CREATED,
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomerRole()]
        return [IsAuthenticated()]


class OutageReportDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAdminRole()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        return Response(OutageReportReadSerializer(_visible_or_404(request.user, pk)).data)

    def patch(self, request, pk):
        report = get_report(pk)
        if report is None:
            raise NotFound("Outage report not found.")
        serializer = AdminOutageUpdateSerializer(report, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            report = update_report_by_admin(report, serializer.validated_data)
        except WorkflowError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(OutageReportReadSerializer(report).data)


class AssignTechnicianView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        report = get_report(pk)
        if report is None:
            raise NotFound("Outage report not found.")
        serializer = AssignTechnicianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            assign_technician(
                report,
                serializer.validated_data["technician"],
                request.user,
                serializer.validated_data.get("notes", ""),
            )
        except WorkflowError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        report = get_report(pk)
        return Response(OutageReportReadSerializer(report).data)


class ProgressUpdateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTechnicianRole()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        report = _visible_or_404(request.user, pk)
        return Response(ProgressUpdateReadSerializer(report.progress_updates.all(), many=True).data)

    def post(self, request, pk):
        report = _visible_or_404(request.user, pk)
        serializer = ProgressUpdateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            progress = add_technician_progress(
                report,
                request.user,
                serializer.validated_data["status"],
                serializer.validated_data["message"],
            )
        except WorkflowError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            ProgressUpdateReadSerializer(progress).data,
            status=status.HTTP_201_CREATED,
        )
