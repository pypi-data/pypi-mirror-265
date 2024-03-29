from qleegss.handler import DataHandler


if __name__ == '__main__':
    eeg_path = r'D:\pythonProject\sleep_stage\dev_test_data\13592029172_0321-22_16_05_0322-08_04_45_2\eeg.eeg'
    acc_path = r'D:\pythonProject\sleep_stage\dev_test_data\13592029172_0321-22_16_05_0322-08_04_45_2\acc.acc'
    sti_path = r'D:\pythonProject\sleep_stage\dev_test_data\13592029172_0321-22_16_05_0322-08_04_45_2\sti.log'
    data = DataHandler(eeg_path, acc_path, sti_path)
    data.load_sti()
