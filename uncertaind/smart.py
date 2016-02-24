""" https://forums.freenas.org/index.php?threads/python-script-to-monitor-drive-temps.22794/
    Modified to work with Python 3.5
"""
import os
import json

class DeviceData():
    device_id = ''
    family = ''
    model = ''
    serial = ''
    firmware_version = ''
    capacity = ''
    sector_sizes = ''
    rotation_rate = ''
    device_is = ''
    ata_version = ''
    sata_version = ''
    smart_support_available = False
    smart_support_enabled = False

class Smart():
    command = 'smartctl'
    device_list = None
    
    def __init__(self):
        self.device_list = self.get_devices()

    def get_data(self, device=None):
        devices = []
        if self.device_list:
            for _device in self.device_list:
                if device and _device not in device:
                    continue
                devices.append(self.get_device_data(_device))
            if devices:
                return json.loads(json.dumps(devices, default=lambda o: o.__dict__))
        return None

    def run_smartctl(self, args):
        command = '{} {}'.format(self.command, args)
        output = os.popen(command).read()
        lines = str.splitlines(output)
        return lines

    def get_devices(self):
        lines = self.run_smartctl('--scan')
        list = []

        for line in lines:
            device_id = str.split(line, ' ', 1)[0]
            list.append(device_id)
        return list

    def get_device_data(self, device_id):
        device_data = DeviceData()
        dev_info_lines = self.run_smartctl('-i {}'.format(device_id))
        device_data.device_id = device_id
        in_info_section = False

        for line2 in dev_info_lines:
            if not in_info_section:
                TheFirstField = str.split(line2, ' ',2)
                if line2.lower() == '=== start of information section ===':
                    in_info_section = True
            else:
                field = str.split(line2,':',1)
                info_title = field[0].lower()

                if info_title == 'model family':
                    device_data.family = field[1].strip()
                elif info_title == 'device model':
                    device_data.model = field[1].strip()
                elif info_title == 'serial number':
                    device_data.serial = field[1].strip()
                elif info_title == 'firmware version':
                    device_data.firmware_version = field[1].strip()
                elif info_title == 'user capacity':
                    device_data.capacity = field[1].strip()
                elif info_title == 'sector sizes':
                    device_data.sector_sizes = field[1].strip()
                elif info_title == 'rotation rate':
                    device_data.rotation_rate = field[1].strip()
                elif info_title == 'device is':
                    device_data.device_is = field[1].strip()
                elif info_title == 'ata version is':
                    device_data.ata_version = field[1].strip()
                elif info_title == 'sata version is':
                    device_data.sata_version = field[1].strip()
                elif info_title == 'smart support is':
                    temp = str.split(field[1].strip(),' ',1)
                    strTemp = temp[0].strip().lower()

                    if strTemp == 'available':
                        device_data.smart_support_available = True
                    elif strTemp == 'unavailable':
                        device_data.smart_support_available = False
                        device_data.smart_support_enabled = False
                    elif strTemp == 'enabled':
                        device_data.smart_support_enabled = True
                    elif strTemp == 'disabled':
                        device_data.smart_support_enabled = False

        return device_data

    """ Requires root
    """
    def get_temperature(self, device_id):
        dev_info_lines = self.run_smartctl('-l scttemp ' + device_id)
        temperature = 0
        for line in dev_info_lines:
            TheFirstField = str.split(line, ' ', 2)
            field = str.split(line, ':', 1)
            if field[0].lower() == 'current temperature':
                temperature = int(field[1].strip().split()[0])
        return temperature