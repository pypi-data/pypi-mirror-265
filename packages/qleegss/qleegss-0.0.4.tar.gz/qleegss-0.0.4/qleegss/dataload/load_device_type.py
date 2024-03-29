"""
加载设备类型
"""


def load_device_type(eeg_path):
    eeg_data = open(eeg_path, 'rb')
    eeg_data.seek(12, 0)
    device_type = int.from_bytes(eeg_data.read(4), byteorder='little', signed=False)
    return device_type
