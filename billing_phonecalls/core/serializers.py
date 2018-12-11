""" modules to serializer models """
from rest_framework import serializers

# from .models.billing import Bill
from .models.phone_calls import Call, CallEvent


class CallSerializer(serializers.ModelSerializer):
    """ Class to Serializer model call """

    type = serializers.ChoiceField(choices=CallEvent.EVENT_TYPES, required=True, write_only=True)
    timestamp = serializers.DateTimeField(required=True, write_only=True)

    def validate(self, data):
        """ method to valid data """
        if data['type'] == 'start':
            if 'source' not in data:
                raise serializers.ValidationError(
                    'This field is required when type is "start"')
            if 'destination' not in data:
                raise serializers.ValidationError(
                    'This field is required when type is "start"')
        return data

    def create(self, validated_data):
        """ Method to create new callEvent """
        phone_call, __ = Call.objects.get_or_create(
            call_id=validated_data.get('call_id'))

        if 'source' in validated_data:
            phone_call.source = validated_data['source']

        if 'destination' in validated_data:
            phone_call.destination = validated_data['destination']

        if not phone_call.valid_type(validated_data.get('type')):
            raise serializers.ValidationError(
                'This call have is event type')

        phone_call.save()

        CallEvent.objects.create(
            call_id=phone_call,
            type_call=validated_data.get('type'),
            timestamp=validated_data.get('timestamp')
        )

        return phone_call

    class Meta:
        """ Meta """
        model = Call
        fields = ('call_id', 'timestamp', 'type', 'source', 'destination')
        extra_kwargs = {
            'source': {'required': False},
            'destination': {'required': False}
        }


class CallBillingSerializer(serializers.ModelSerializer):
    """ Class to Serializer model call billing """

    call_start_date = serializers.SerializerMethodField()
    call_start_time = serializers.SerializerMethodField()

    def get_call_start_date(self, obj):
        """ return date to start date of call """
        return obj.start_time.date()

    def get_call_start_time(self, obj):
        """ return time to start date of call """
        return obj.start_time.time()

    class Meta:
        """ Meta """
        model = Call
        fields = ('destination', 'call_start_date', 'call_start_time', 'format_duration', 'price')


class TelephoneBillSerializer(serializers.Serializer):
    """ Class to Serializer model telephone billing """

    telephone = serializers.CharField(read_only=True)
    period = serializers.CharField(read_only=True)
    calls = CallBillingSerializer(read_only=True, many=True)
