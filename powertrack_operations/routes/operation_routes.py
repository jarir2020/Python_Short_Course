"""Route registration for PowerTrack operations and public status."""

from fastapi import APIRouter

from ..controllers import (
    read_operations_summary,
    read_public_outages,
    read_technician_queue,
)
from ..models import OperationsSummary, PublicOutage, TechnicianQueue


router = APIRouter(tags=["powertrack-operations"])

router.add_api_route(
    "/operations/summary",
    read_operations_summary,
    methods=["GET"],
    response_model=OperationsSummary,
)
router.add_api_route(
    "/operations/technicians/{technician_id}/queue",
    read_technician_queue,
    methods=["GET"],
    response_model=TechnicianQueue,
)
router.add_api_route(
    "/public/outages",
    read_public_outages,
    methods=["GET"],
    response_model=list[PublicOutage],
)
