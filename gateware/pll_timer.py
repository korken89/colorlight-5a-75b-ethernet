from amaranth import Elaboratable, Signal, Module, ClockSignal, Instance
from amaranth.build import Platform
from amaranth.lib.fifo import AsyncFIFOBuffered
from .ecp5pll import ECP5PLL, ECP5PLLConfig


class PllTimer(Elaboratable):
    def elaborate(self, platform: Platform):
        led1 = platform.request("led", 0)#, xdr=2)
        # led4 = platform.request("led", 3)

        w = 8
        

        timer1 = Signal(25)
        fifo_buf = Signal(w)

        led_sig = Signal()

        m = Module()

        m.submodules.pll = ECP5PLL(clock_signal_name="clk25",
                                   clock_config=[
                                       ECP5PLLConfig("fast", 125),
                                       ECP5PLLConfig("sync", 25),
                                   ])

        # Delay
        m.submodules.delay = Instance("DELAYG",
                    p_DEL_MODE  = "SCLK_ALIGNED",
                    p_DEL_VALUE = 200,
                    i_A         = led_sig,
                    o_Z         = led1.o,
                )

        # This should use 2 EBRs
        m.submodules.fifo = fifo = AsyncFIFOBuffered(
            width=w, depth=2049, r_domain="fast", w_domain="sync", exact_depth=True)

        # Write the FIFO using the timer data
        m.d.sync += timer1.eq(timer1 + 1)

        with m.If(fifo.w_rdy):
            m.d.comb += fifo.w_data.eq(timer1[25-w:25])
        m.d.comb += fifo.w_en.eq(1)

        # Read the FIFO in the `fast` domain, the LEDs should blink at the same time
        with m.If(fifo.r_rdy):
            m.d.fast += fifo_buf.eq(fifo.r_data)

        m.d.comb += fifo.r_en.eq(1)

        # Combinatorial logic
        m.d.comb += led_sig.eq(fifo_buf[-1])

        return m
