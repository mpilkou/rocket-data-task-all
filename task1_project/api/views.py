import logging

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.parsers import JSONParser

from drf_yasg.utils import swagger_auto_schema

from django.core.exceptions import ValidationError
from django.db.models import Avg, DecimalField, Q
from django.contrib.auth.models import User

from api.models import Chain, Contact, Product
from api.serializers import ChainSerializer, ContactSerializer, ProductSerializer

logger = logging.getLogger(__name__)

# Create your views here.
@swagger_auto_schema(
        methods=['put','post'],
        request_body=ChainSerializer,
        )
@api_view(['GET','PUT','POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def get_chains_network(request):
    content = {}
    if request.method == 'GET':
        all_chains = list(Chain.objects.all())
        serialized_all_chains = ChainSerializer(data=all_chains, many=True)
        serialized_all_chains.is_valid()
        content = {
            'network': serialized_all_chains.data,
        }
    elif request.method == 'PUT':
        request.data['user'] = request.user.id
        chain_serializer = ChainSerializer(data=request.data)
        if not chain_serializer.is_valid():
            return Response(data = {'detail' : chain_serializer.errors}, status=400)

        try:
            chain_serializer.create(chain_serializer.validated_data)
        except ValidationError as validation_error:
            return Response(data = {'detail' : validation_error}, status=400)

        content = chain_serializer.data
        return Response(content, status=201)
    elif request.method == 'POST':
        request.data['user'] = request.user.id

        try:
            chech_id = request.data['id']
        except KeyError:
            return Response(data = {'detail' : 'Request does not have id to update'}, status=400)

        try:
            chain_before_update = Chain.objects.get(id=chech_id)
        except Chain.DoesNotExist:
            return Response(data = {'detail' : 'Chain with this id does not exists'}, status=400)
        request.data['debt'] = chain_before_update.debt
        chain_serializer = ChainSerializer(instance = chain_before_update, data=request.data)
        if not chain_serializer.is_valid():
            return Response(data = {'detail' : chain_serializer.errors}, status=400)
        try:
            chain_serializer.save()
        except ValidationError as validation_error:
            return Response(data = {'detail' : validation_error}, status=400)

        content = chain_serializer.data
        return Response(content, status=201)
    return Response(content, status=201)

@swagger_auto_schema(
        methods=['delete'],
        )
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def delete_chain(request, chain_id):
    try:
        chain = Chain.objects.get(id = chain_id)
    except Chain.DoesNotExist:
        return Response(data = {'detail' : 'Chain with this id does not exists'}, status=400)

    try:
        chain.staff.get(id = request.user.id)
    except User.DoesNotExist:
        return Response(data = {'detail' : 'Forbidden'}, status=403)

    chain.delete()
    return Response(status=201)


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
    q_obj = Q(chain__debt__gt=avg_debt)
    filtered_chains = Chain.objects.filter(q_obj)
    serialized_chains = ChainSerializer(data=filtered_chains, many=True)
    serialized_chains.is_valid()

    content = {
        'network': serialized_chains.data,
    }
    return Response(content, status=201)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, ])
@permission_classes([IsAuthenticatedOrReadOnly, IsAuthenticated, ])
def get_chain_contacts_by_product_id(_, product_id):
    chain_id = Product.objects.get(id=product_id).chain.id
    contacts = Contact.objects.filter(chain_fk__id=chain_id)
    # contacts = Contact.objects.filter(chain_fk__id=chain_id)
    serialized_chains = ContactSerializer(data=contacts, many=True)
    serialized_chains.is_valid()
    content = {
        'network': serialized_chains.data,
    }
    return Response(content, status=201)


