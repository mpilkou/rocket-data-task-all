import logging

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.db.models import Avg, DecimalField, Q

from api.models import Chain, Contact
from api.serializers import ChainSerializer

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def get_all_network_chains(_):
    all_chains = list(Chain.objects.all())
    serialized_all_chains = ChainSerializer(data=all_chains, many=True)
    serialized_all_chains.is_valid()
    content = {
        'network': serialized_all_chains.data,
    }
    return Response(content, status=201)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def get_chains_by_country(_, country):
    filtered_chains = []

    for contact in Contact.objects.filter(country=country):
        filtered_chains.append(Chain.objects.get(id = contact.chain_fk.id))
    serialized_chains = ChainSerializer(data=filtered_chains, many=True)
    serialized_chains.is_valid()

    content = {
        'network': serialized_chains.data,
    }
    return Response(content, status=201)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def get_chains_by_gt_avg_debt(_):
    
    avg_debt = Chain.objects.aggregate(avg=Avg('debt', output_field=DecimalField()))['avg']
    q = Q(chain__debt__gt=avg_debt)
    filtered_chains = Chain.objects.filter(q)
    serialized_chains = ChainSerializer(data=filtered_chains, many=True)
    serialized_chains.is_valid()

    content = {
        'network': serialized_chains.data,
    }
    return Response(content, status=201)
