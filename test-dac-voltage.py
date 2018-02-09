from shimcontrol.lib import DACCommandSet
import time

values = list(range(0x0000, 0x10000, 0x200)) + [0xffff]

for value in values:
	dac = DACCommandSet(5)
	dac.from_write([(0, value)])
	dac.execute()
	print('\a')

	output = '{}'.format(hex(value))
	print(output)
	
	time.sleep(6)
