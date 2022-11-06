import logging
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from django.shortcuts import render
# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required


# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def test(req):
    logger = logging.getLogger(__name__)
    logger.debug(req.data.get)
    content = {
            'test': 'test',
        }

    return Response(content, status=201)
