from rest_framework import generics, permissions
from finances.serializers.insurance import InsuranceSerializer
from finances.models.insurance import Insurance
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


class InsuranceCreateView(generics.CreateAPIView):
    serializer_class = InsuranceSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Insurance.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        message = render_to_string('emails/insurance_form_receive.html', {
            'user': serializer.data['email'],
        })
        send_mail('Thank you for using rntdel',message,settings.EMAIL_HOST_USER, [serializer.data['email']],  fail_silently=False,)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)