# Project-level tests

Django discovers app tests through each app's test module. The first
PowerTrack workflow tests therefore live in `outages/tests.py`. This directory
is reserved for tests that span multiple apps, such as a future integration
test for Django and the read-only FastAPI service.
