from rest_framework import generics, permissions
from finances.serializers.loan import LoanSerializer
from finances.models.loan import Loan
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


class LoanCreateAPIView(generics.CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Loan.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        message = render_to_string('emails/loan_form_receive.html', {
            'user': serializer.data['email'],
        })
        send_mail('Thank you for using meetquoteshack',message,settings.EMAIL_HOST_USER, [serializer.data['email']],  fail_silently=False,)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)