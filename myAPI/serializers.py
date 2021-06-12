from rest_framework import serializers
from .models import Approval

# to create json file

class ApprovalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'


