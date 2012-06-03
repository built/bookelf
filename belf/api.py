from tastypie.resources import ModelResource
from belf.models import School, Need

class SchoolResource(ModelResource):
    class Meta:
        queryset = School.objects.all()


class NeedResource(ModelResource):
    class Meta:
        queryset = Need.objects.all()
