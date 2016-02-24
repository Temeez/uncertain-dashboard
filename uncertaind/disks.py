import os
import shutil
from collections import namedtuple

from uncertaind.smart import Smart

class Disks():
    SMART = Smart()
    disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
    usage_ntuple = namedtuple('usage',  'total used free percent')

    def get_smart_data(self):
        return self.SMART.get_data()

    def get_disks(self, sort=True, device=None):
        disk_list = []

        for partition in self.get_partitions():
            if device and device not in partition.device:
                continue
            usage = self.get_usage(partition.mountpoint)
            dict = {
                'physical': partition.device[:-1],
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'temperature': self.SMART.get_temperature(partition.device)
            }
            disk_list.append(dict)

        if sort:
            disk_list = sorted(disk_list, key=lambda k: k['physical'])
        if disk_list:
            return disk_list
        else:
            return {
                'result': False,
                'reason': 'Disk not found'
            }, 404

    def get_partitions(self, all=False):
        """Return all mounted partitions as a nameduple.
        If all == False return phyisical partitions only.
        """
        phydevs = []
        f = open("/proc/filesystems", "r")
        for line in f:
            if not line.startswith("nodev"):
                phydevs.append(line.strip())

        retlist = []
        f = open('/etc/mtab', "r")
        for line in f:
            if not all and line.startswith('none'):
                continue
            fields = line.split()
            device = fields[0]
            mountpoint = fields[1]
            fstype = fields[2]
            if not all and fstype not in phydevs:
                continue
            if device == 'none':
                device = ''
            ntuple = self.disk_ntuple(device, mountpoint, fstype)
            retlist.append(ntuple)
        return retlist

    def get_usage(self, path):
        """Return disk usage associated with path."""
        usage = shutil.disk_usage(path)

        # Usage in GB (1000^3)
        total = usage.total / 1000000000
        used = usage.used / 1000000000
        free = usage.free / 1000000000

        try:
            percent = ret = (float(used) / total) * 100
        except ZeroDivisionError:
            percent = 0

        return self.usage_ntuple(total, used, free, int(round(percent, 0)))