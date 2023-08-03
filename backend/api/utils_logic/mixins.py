from rest_framework import mixins, viewsets


class CreateCastomView(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
