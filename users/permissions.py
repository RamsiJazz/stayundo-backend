#users/permissions.py
from .permissions import IsAdminOnly

class UserViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'patch', 'head', 'options']