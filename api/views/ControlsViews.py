from gossips.models import GossipsModel
from rest_framework.generics import (
    ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, 
    RetrieveAPIView, 
)
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from controls.models import FalseInformation, RFRModel, FeedbackModel
from ..serializers import ControlsSerializer
from ..serializers.GossipSerializers import GossipListCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .. import pagination


def get_object_or_rest_404(klass, msg="NotFound", **kwargs):
    qs = klass.objects.filter(**kwargs)
    if qs.exists():
        return qs.get()

    raise NotFound(msg)


def get_slug(self):
    return self.kwargs.get(self.lookup_url_kwarg)


class FalseInformationListAPIView(ListAPIView):
    serializer_class = GossipListCreateSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = pagination.Results10SetPagination

    def get_false_gossips(self):
        qs = GossipsModel.objects.all()
        lst = []
        for i in qs:
            total = i.true.count() + i.false.count()
            if total > 1000:
                lst.append(i)


        return sorted(lst, key=lambda x: x.false.count(), reverse=True)

    def get_queryset(self):
        false_gossips = self.get_false_gossips()
        return GossipsModel.objects.all().order_by("date_published")[:3]


class FalseInformationCreateAPIView(CreateAPIView):
    serializer_class = ControlsSerializer.FalseInformationListSerializer
    permission_classes = [AllowAny, ]
    lookup_url_kwarg = "gossip_slug"

    def perform_create(self, serializer):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        gossip = get_object_or_rest_404(GossipsModel, slug=slug)        
        return serializer.save(gossip=gossip)


class FalseInformationRetrieveAPIView(RetrieveAPIView):
    serializer_class = ControlsSerializer.FalseInformationListSerializer
    lookup_url_kwarg = "false_id"
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        try:
            false_id = int(get_slug(self))
        except ObjectDoesNotExist:
            raise PermissionDenied("Id should be an Integer...")

        false_mdl = get_object_or_rest_404(FalseInformation, id=false_id, msg="Error finding Feedback with this Info...")
        return false_mdl


class RFRModelListAPIView(ListAPIView):
    serializer_class = ControlsSerializer.RFRModelSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = pagination.Results10SetPagination

    def get_queryset(self):
        qs = RFRModel.objects.all()
        return qs


class RFRModelCreateAPIView(CreateAPIView):
    serializer_class = ControlsSerializer.RFRModelSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "gossip_slug"

    def perform_create(self, serializer):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        gossip = get_object_or_rest_404(GossipsModel, slug=slug)
        user = self.request.user
        if user == gossip.author:
            raise PermissionDenied("User cannot condemn his own gossips...")

        serializer.save(gossip=gossip, user=user)


class RFRModelRetrieveAPIView(RetrieveAPIView):
    serializer_class = ControlsSerializer.RFRModelSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_url_kwarg = "rfr_model_id"

    def get_queryset(self):
        pass

    def get_rfr_obj(self):
        rfr_id = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_rest_404(RFRModel, id=rfr_id)
        return obj

    def get_object(self):
        return self.get_rfr_obj()


class FeedbackListCreateAPIView(ListCreateAPIView):
    serializer_class = ControlsSerializer.FeedbackModelSerializer
    pagination_class = pagination.Results10SetPagination
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        qs = FeedbackModel.objects.all()
        return qs


class FeedbackRetrieveAPIView(RetrieveAPIView):
    serializer_class = ControlsSerializer.FeedbackModelSerializer
    lookup_url_kwarg = "feedback_id"
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        feed_id = get_slug(self)
        obj = get_object_or_rest_404(FeedbackModel, id=feed_id)
        return obj

