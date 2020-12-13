from rest_framework import serializers,fields
from finances.models.insurance import Insurance


class InsuranceSerializer(serializers.ModelSerializer):
    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Insurance
        fields = '__all__'