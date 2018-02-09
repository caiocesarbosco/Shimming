import random
import unittest

from shimcontrol.lib import DACNop, DACWrite, DACCommandSet


class DACTests(unittest.TestCase):
    def setUp(self):
        random.seed('shimcontrol')
        self.maxDiff = None

    def test_nop(self):
        for dacs_available in range(1, 6):
            nop = DACNop()

            self.assertEqual(
                nop.serialize(dacs_available),
                [0xaa, 0xff, 0xaa, 0xaa]
            )

    def test_write_update(self):
        for dacs_available in range(1, 6):
            for channel in range(8 * dacs_available):
                for value in range(0x0000, 0x10000, 0x1000):
                    write = DACWrite(channel, value, update=True)
                    data = write.serialize(dacs_available)
                    self.assertEqual(data[1] & 0b00110000, 0b00110000)

                    write = DACWrite(channel, value, update=False)
                    data = write.serialize(dacs_available)
                    self.assertNotEqual(data[1] & 0b00110000, 0b00110000)

    def test_write_dac(self):
        for channel in range(40):
            write = DACWrite(channel, random.randint(0, 0xffff))

            self.assertEqual(write.dac, channel // 8)

    def test_dac_write_set(self):
        # um dac só
        dac_write_set = DACCommandSet(1)
        output = dac_write_set.from_write(
            [[5, 0x1234], [2, 0x4321]]
        )

        self.assertEqual(
            output,
            [
                [DACWrite(5, 0x1234)],
                [DACWrite(2, 0x4321)]
            ]
        )

        # dois dacs
        dac_write_set = DACCommandSet(2)
        output = dac_write_set.from_write(
            [[5, 0x1234], [15, 0x4321], [10, 0xaaaa]]
        )

        self.assertEqual(
            output,
            [
                [DACWrite(5, 0x1234), DACWrite(15, 0x4321)],
                [DACNop(), DACWrite(10, 0xaaaa)]
            ]
        )

        # cinco dacs
        dac_write_set = DACCommandSet(5)
        output = dac_write_set.from_write([
            (8, 0xaaaa), (10, 0xbbbb), # comandos pro dac 2
            (16, 0xcccc), (18, 0xdddd), (20, 0xeeee), #comandos pro dac 3
            (24, 0xffff), # comandos pro dac 4
        ])

        self.assertEqual(
            output,
            [
                [
                    DACNop(),
                    DACWrite(8, 0xaaaa),
                    DACWrite(16, 0xcccc),
                    DACWrite(24, 0xffff),
                    DACNop(),
                ],
                [
                    DACNop(),
                    DACWrite(10, 0xbbbb),
                    DACWrite(18, 0xdddd),
                    DACNop(),
                    DACNop(),
                ],
                [
                    DACNop(),
                    DACNop(),
                    DACWrite(20, 0xeeee),
                    DACNop(),
                    DACNop(),
                ]
            ]
        )

