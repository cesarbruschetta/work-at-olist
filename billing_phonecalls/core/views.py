""" module to views of core """

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CallSerializer


class RegisterCallEventApi(APIView):
    """ Create a start or end event call of record. """

    def post(self, request):
        """ Method to post event """

        serializer = CallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
