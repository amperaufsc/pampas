### RES (Vehicle Module):

The **RES (Remote Emergency System)** lets an outside operator stop the vehicle remotely, independent of the driver or the onboard software. It consists of two boards: a receiver with an STM32WL5M radio MCU, which gets the stop command over RF, and a vehicle module built around an STM32F103C8T6, mated to the receiver through a shield connector. On command, the vehicle module opens the Shutdown Circuit loop to cut power to the inverter and contactors, and switches the EBS supply to engage the autonomous braking system. It interfaces with the rest of the system through the Placão, for power, CAN and the Shutdown Circuit, and through a dedicated output to the EBS.

<img width="960" height="655" alt="Image" src="https://github.com/user-attachments/assets/f3193705-9994-4583-b31a-66fe19ac004a" />

**Inputs:**

- **Power:**
  - `12V` (`Alimentação.4`): main 12 V supply, equivalent to `VCC_RES` from the Placão's eFuse. Feeds the buck converter (`IC1`) and, downstream, the whole board.
  - `12V_EBS` (`Alimentação.3`): dedicated 12 V supply coming from the Placão, feeds the EBS-cutoff relay circuit.
  - `GND` (`Alimentação.1`, `J10.1–4`, `J11.1–4`).
- **Shutdown Circuit:** `SC_IN` (`CAN e SC.2`): SDC signal coming from the Placão (and ultimately from the RES on the Placão's own RES header), routed to the common pin of relay `K2`.
- **CAN bus:** `CAN_HIGH` (`CAN e SC.4`) and `CAN_LOW` (`CAN e SC.3`): vehicle CAN bus, received by the onboard transceiver (`U2`) and read by the STM32F103 (`U1`).
- **Relay control (from the STM32WL5M shield):** signals named `K1` (shield pin 7) and `K2` (shield pin 5), driving the gate circuits of `Q2` and `Q1` respectively. These come directly from the companion radio board, not from `U1`.
- **Serial link (from the STM32WL5M shield):** `USART1_RX` (shield pin 18).
- **Debug/Programming:** `SWDIO`, `SWCLK` (header `SW`) and `BOOT_0`, `BOOT_1` (dedicated headers), used to flash and debug `U1`.

**Outputs:**

- **Shutdown Circuit:** `SC_OUT_RES` (`CAN e SC.1`): SDC signal after passing through relay `K2`, forwarded back to the Placão (and from there to the DSB).
- **CAN bus:** `CAN_HIGH` / `CAN_LOW` (`CAN e SC.4` / `CAN e SC.3`): messages transmitted by `U1` on the vehicle CAN bus (bidirectional with the input above).
- **EBS output connector (`SC_EBS`):** `12V_EBS` (pin 1) and `SC_OUT_RES` (pin 2), routed onward to the external EBS/ASB circuitry.
- **CAN output connector (`CAN`, MicroFit 3x2):** `GND`, `CAN_LOW`, `SC_IN`, `CAN_HIGH`, `12V` — appears to duplicate the signals above for an external tap or test point.
- **Serial link (to the STM32WL5M shield):** `USART1_TX` (shield pin 16).
- **Status LEDs (onboard, not off-board):** `CAN_LED`, `LED_Builtin`, and individual rail/signal indicators for `12V`, `12V_EBS`, `5V`, `3V3` and `SC_OUT_RES`.
