import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["iceberg"]


class iceberg(LatticeICE40Platform):
    device      = "iCE40HX4K"
    package     = "TQ144"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("49", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="62 56 44 47", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs="71", clk="70", mosi="68", miso="67",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("pmod", 1, "38 39 34 37 - - 32 33 29 31 - -"),  # Bank A
		Connector("pmod", 2, "23 24 19 22 - - 17 18 15 16 - -"),  # Bank B
        Connector("pmod", 3, "12 11 10 9 - - 8 7 4 3 - -"), # Bank C
        Connector("pmod", 4, "1 2 143 144 - - 141 142 138 139 - -"), # Bank D
		Connector("pmod", 5, "121 120 119 118 - - 117 116 115 110 - -"),  # Bank E
		Connector("pmod", 6, "106 107 104 105 - - 101 102 98 99 - -"),  # Bank F
		Connector("pmod", 7, "96 97 91 95 - - 85 90 83 84 - -"),  # Bank G
		Connector("pmod", 8, "82 81 80 79 - - 78 76 75 73 - -"),  # Bank H
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    iceberg().build(Blinky(), do_program=True)
