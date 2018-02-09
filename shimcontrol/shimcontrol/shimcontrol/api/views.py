from rest_framework.views import APIView
from rest_framework.response import Response

from shimcontrol.lib import dac_code_to_voltage, ADCCommandSet, DACCommandSet


class ADCView(APIView):
    def get(self, request, format=None):
        channels = request.query_params.get('channels')
        channels = [int(ch) for ch in channels.split(',')]

        adc = ADCCommandSet(5)
        adc.from_read(channels)

        results = adc.execute()

        return Response(results)

class DACView(APIView):
    def post(self, request, format=None):
        data = request.data.get('channels')

        dac = DACCommandSet(5)
        dac.from_write(data)
        dac.execute()

        results = [(ch, dac_code_to_voltage(code)) for ch, code in data]
        return Response(results)
