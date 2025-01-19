from amaranth import Elaboratable, Signal, Module
from amaranth.build import Platform
from amaranth.lib.fifo import AsyncFIFOBuffered
from .ecp5pll import ECP5PLL, ECP5PLLConfig


class PllTimer(Elaboratable):
    def elaborate(self, platform: Platform):
        led1 = platform.request("led", 0)
        # led4 = platform.request("led", 3)

        timer1 = Signal(25)
        fifo_buf = Signal(16)

        m = Module()

        # Connect pseudo power pins for the FT600 and DDR3 banks

        m.submodules.pll = ECP5PLL(clock_signal_name="clk25",
                                   clock_config=[
                                       ECP5PLLConfig("sync", 25),
                                       ECP5PLLConfig("fast", 100, error=0),
                                   ])

        m.submodules.fifo = fifo = AsyncFIFOBuffered(
            width=16, depth=1024, r_domain="fast", w_domain="sync")

        # Write the FIFO using the timer data
        m.d.sync += timer1.eq(timer1 + 1)
        with m.If(fifo.w_rdy):
            m.d.comb += fifo.w_data.eq(timer1[9:25])
        m.d.comb += fifo.w_en.eq(1)

        # Read the FIFO in the `fast` domain, the LEDs should blink at the same time
        with m.If(fifo.r_rdy):
            m.d.fast += fifo_buf.eq(fifo.r_data)

        m.d.comb += fifo.r_en.eq(1)

        # Combinatorial logic
        m.d.comb += led1.o.eq(timer1[-1])
        # m.d.comb += led4.o.eq(fifo_buf[-1])

        return m
