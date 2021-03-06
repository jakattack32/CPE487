
# Lab 2: Four-Digit Hex Counter

* Build a four-digit (16-bit) counter to display its value on 7-segment displays (See Section 9.1 Seven-Segment Display of the [Refenece Manual](https://reference.digilentinc.com/_media/reference/programmable-logic/nexys-a7/nexys-a7_rm.pdf))

![mpx.png](https://github.com/kevinwlu/dsd/blob/master/Nexys-A7/Lab-2/mpx.png)

![counter.png](https://github.com/kevinwlu/dsd/blob/master/Nexys-A7/Lab-2/counter.png)

![hexcount.png](https://github.com/kevinwlu/dsd/blob/master/Nexys-A7/Lab-2/hexcount.png)

* The counter module generates a 16-bit count value using bits 23 to 38 of the 39-bit binary counter at a frequency of 100 MHz / 2<sup>23</sup> ≈ 12 Hz with a complete cycle taking approximately 16<sup>4</sup> / 12 ≈ 5461 seconds or 91 minutes

* The binary counter bits 17 and 18 generate a 0 to 3 count sequence at a frequency of 100 MHz / 2<sup>17</sup> ≈ 763 Hz

* The sequence repeats at a frequency of approximately 763 Hz / 4  ≈ 191 Hz that is fast enough to eliminate any visual flicker in the displays.

* This multiplexing is fast enough (at least 60 complete cycles per second) to appear as if all four displays are continuously illuminated – each with their own four bits of information.

* The mpx output from the new counter module now drives the dig input of the leddec module.

* The mpx signal is also used to select which 4-bits of the 16-bit count output should be sent to the data input of the leddec module.

* By time multiplexing the 7-segment displays that share the same cathode lines (CA to CG), four different digits can appear on one display at a time.
  * Turn on display 0 for a few milliseconds by enabling its common anode AN0 and decoding count (0~3) to drive the cathode lines.
  * Switch to display 1 for a few milliseconds by turning off AN0, turning on AN1 and decoding count (4~7) to drive the cathode lines.
  * Shift to display 2 for a few milliseconds and then finally display 3 for a few milliseconds, after that go back and start again at display 0.
  * Each digit is thus illuminated only one quarter of the time
