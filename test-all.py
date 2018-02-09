from shimcontrol.lib import ADCCommandSet, DACCommandSet

def find_if(sequence, value, key=None):
	if key is not None:
		for item in sequence:
			if key(item) == value:
				return item
		else:
			raise ValueError
	else:
		if value in sequence:
			return value
		else:
			raise ValueError

DAC_CHANNEL = 0
ADC_CHANNEL = 10

values = list(range(0x0000, 0x10000, 0x200)) + [0xffff]

for value in values:
	expected = 4.096 - (2 * 4.096) * (value / float(0xffff))

	dac = DACCommandSet(5)
	dac.from_write([(DAC_CHANNEL, value)])
	dac.execute()

	adc = ADCCommandSet(5)
	adc.from_read([ADC_CHANNEL])
	results = adc.execute()

	adc_value = - find_if(results, ADC_CHANNEL, key=lambda x: x[0])[1]

	output = '0x{:04X} {:2.4f} {:2.4f}'.format(value, expected, adc_value)
	print(output)
