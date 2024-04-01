"""
加载acc数据
"""
import numpy as np


def load_acc(acc_path):
    acc_data = open(acc_path, 'rb')
    acc_len = len(acc_data.read())
    acc_data.seek(8, 0)
    length = int.from_bytes(acc_data.read(4), byteorder='little', signed=False)
    acc_data.seek(length, 0)
    all_package = np.array(list(acc_data.read(acc_len - length)))
    acc_data.seek(21, 0)
    sample_count = int.from_bytes(acc_data.read(4), byteorder='little', signed=False)
    acc_data.seek(16, 0)
    point_bytes = int.from_bytes(acc_data.read(1), byteorder='little', signed=False)
    channel_count = 3  # NOTE: 3通道
    package_length = sample_count * point_bytes * channel_count + 18
    all_package = all_package.reshape(-1, package_length)
    all_package_data = all_package[:, 18:package_length]
    all_package_data = all_package_data.reshape(-1, point_bytes)
    all_package_data = all_package_data[:, 0] + all_package_data[:, 1] * 256
    raw_data = np.squeeze(all_package_data)
    data = np.transpose(raw_data.reshape(-1, channel_count))
    acc = data - 32767
    acc = acc[:, : (acc.shape[1] // (15 * 50)) * (15 * 50)]
    return acc
