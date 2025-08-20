from nidaqmx.system import System
import nidaqmx

# system = System.local()
# for device in system.devices:
#     print(f"Device: {device.name} ({device.product_type})")
#     print("  AI channels:", [chan.name for chan in device.ai_physical_chans])
#     print("  AO channels:", [chan.name for chan in device.ao_physical_chans])
#     print("  DI lines:", [line.name for line in device.di_lines])
#     print("  DO lines:", [line.name for line in device.do_lines])
#     print("  Counters:", [chan.name for chan in device.co_physical_chans])

print("Scanning AI channels for signal...")

with nidaqmx.Task() as task:
    for i in range(32):  # ai0 to ai31
        chan = f"Dev1/ai{i}"
        try:
            task.ai_channels.add_ai_voltage_chan(chan)
            value = task.read()
            print(f"{chan}: {value:.3f} V")
            task.ai_channels.clear()  # Clear before next channel
        except Exception as e:
            print(f"{chan}: Error reading ({e})")
