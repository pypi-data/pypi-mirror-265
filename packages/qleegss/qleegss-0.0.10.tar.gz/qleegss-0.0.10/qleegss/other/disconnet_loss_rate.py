# all_package_time = all_package[:, 2:10]
# all_package_id = all_package[:, 10:14]
#
# # computing package loss rate/disconnection rate
# all_package_id = all_package_id.astype(np.uint8)
# all_package_id = np.apply_along_axis(int_from_bytes_4bit, axis=1, arr=all_package_id)
# all_package_id = all_package_id.astype(np.int32)
#
# all_package_time = all_package_time.astype(np.uint8)
# all_package_time = np.apply_along_axis(int_from_bytes_8bit, axis=1, arr=all_package_time)
# all_package_time = all_package_time.astype(np.int32)
#
# package_time_interval = all_package_time[1:] - all_package_time[:-1]
# disconnect_point = np.where(package_time_interval > 3000)[0]
#
# disconnection_sum = 0
#
# package_segment = [0]
# if disconnect_point is not None and len(disconnect_point) > 0:
#     for i in range(len(disconnect_point)):
#         package_segment.append(disconnect_point[i])
#         package_segment.append(disconnect_point[i] + 1)
#         disconnection_sum += all_package_time[disconnect_point[i] + 1] - all_package_time[disconnect_point[i]]
#
# disconnect_rate = disconnection_sum / all_package_time[-1]
#
# package_segment.append(all_package_id.shape[0] - 1)
# package_segment = np.array(package_segment).reshape([-1, 2])
#
# package_sum = 0
# loss_package_sum = 0
# for i in range(package_segment.shape[0]):
#     left = package_segment[i][0]
#     right = package_segment[i][1]
#     package_sum += all_package_id[right] - 0 + 1
#     loss_package_sum += all_package_id[right] - 0 + 1 - (right - left + 1)
# package_loss_rate = loss_package_sum / package_sum
