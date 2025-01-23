import board
import digitalio
import storage
import usb_cdc
import usb_midi
import usb_hid

# Modified boot descriptor to enable RP2040 macropad to work with KVM switch
# https://github.com/adafruit/circuitpython/issues/1136#issuecomment-1002833056
BOOT_KEYBOARD_DESCRIPTOR=bytes((
0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
0x09, 0x06,        # Usage (Keyboard)
0xA1, 0x01,        # Collection (Application)
0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
0x19, 0xE0,        #   Usage Minimum (0xE0)
0x29, 0xE7,        #   Usage Maximum (0xE7)
0x15, 0x00,        #   Logical Minimum (0)
0x25, 0x01,        #   Logical Maximum (1)
0x75, 0x01,        #   Report Size (1)
0x95, 0x08,        #   Report Count (8)
0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Pr
0x95, 0x01,        #   Report Count (1)
0x75, 0x08,        #   Report Size (8)
0x81, 0x01,        #   Input (Const,Array,Abs,No Wrap,Linear
0x95, 0x03,        #   Report Count (3)
0x75, 0x01,        #   Report Size (1)
0x05, 0x08,        #   Usage Page (LEDs)
0x19, 0x01,        #   Usage Minimum (Num Lock)
0x29, 0x05,        #   Usage Maximum (Kana)
0x91, 0x02,        #   Output (Data,Var,Abs,No Wrap,Linear,P
0x95, 0x01,        #   Report Count (1)
0x75, 0x05,        #   Report Size (5)
0x91, 0x01,        #   Output (Const,Array,Abs,No Wrap,Linea
0x95, 0x06,        #   Report Count (6)
0x75, 0x08,        #   Report Size (8)
0x15, 0x00,        #   Logical Minimum (0)
0x26, 0xFF, 0x00,  #   Logical Maximum (255)
0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
0x19, 0x00,        #   Usage Minimum (0x00)
0x2A, 0xFF, 0x00,  #   Usage Maximum (0xFF)
0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,
0xC0,              # End Collection
))

maintenance_pin = digitalio.DigitalInOut(board.GP2)
maintenance_pin.direction = digitalio.Direction.INPUT
maintenance_pin.pull = digitalio.Pull.UP
maintenance_mode = not maintenance_pin.value # active low

# Keyboard object using modified boot descriptor
kbd = usb_hid.Device(
    report_descriptor=BOOT_KEYBOARD_DESCRIPTOR,
    usage=0x06,
    usage_page=0x01,
    report_ids=(0,),
    in_report_lengths=(8,),
    out_report_lengths=(1,),
)

if maintenance_mode:
    print("Booting in maintenance mode")
    print("All USB devices enabled")
else:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((kbd,), boot_device=1)
