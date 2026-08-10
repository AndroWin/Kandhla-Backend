"""
Republic of Kandhla - Global Utility Functions
Custom exception handler aur common helpers yahan define hain.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Global DRF exception handler.
    Har unhandled error ko log karta hai aur clean JSON response deta hai.
    INSTRUCTIONS.md ke mutabiq: Global exception handlers implement karo
    to prevent unexpected app crashes.
    """
    # Pehle DRF ka default handler call karo
    response = exception_handler(exc, context)

    if response is not None:
        # Standard DRF errors ko structured format mein wrap karo
        custom_response = {
            'success': False,
            'error': {
                'status_code': response.status_code,
                'detail': response.data,
            }
        }
        response.data = custom_response
    else:
        # Unhandled exceptions — 500 Internal Server Error
        logger.exception(
            f"Unhandled exception in {context.get('view', 'unknown_view')}: {exc}"
        )
        response = Response(
            {
                'success': False,
                'error': {
                    'status_code': 500,
                    'detail': 'Internal server error. Humari team ko notify kar diya gaya hai.',
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
