""" module to views of core """

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CallSerializer, TelephoneBillSerializer
from .utils import last_period, valid_period
from .models.phone_calls import Call


class RegisterCallEventApi(APIView):
    """ Create a start or end event call of record. """

    def post(self, request):
        """ Method to post event """

        serializer = CallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TelephoneBillApi(APIView):
    """ view to return list of calls in of period """

    def get(self, request, telephone, **kwargs):
        """ method to list of calls """
        query = self.request.query_params

        year = query.get('year')
        month = query.get('month')

        if not valid_period(year, month):
            return Response({'detail': "Period is invalid, period not closed."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not month and not year:
            year, month = last_period()

        result = Call.objects.get_telephone_bill(telephone, year, month)

        serializer = TelephoneBillSerializer({
            "telephone": telephone,
            "period": "%s/%s" % (month, year),
            "calls": result
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
