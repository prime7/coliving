from rest_framework import serializers,fields
from finances.models.loan import Loan


class LoanSerializer(serializers.ModelSerializer):
    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Loan
        fields = '__all__'