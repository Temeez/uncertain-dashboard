import os
import pytest
import dbus # Just to make sure its installed, might not be needed
from uncertaind.services import sys_manager, Services
from uncertaind.models import Service
from uncertaind.disks import Disks
from uncertaind.api import Service as Service_API
from uncertaind.api import Disks as Disks_API

INVALID_DISK_NAME = 'foo'
INVALID_SERVICE_NAME = 'foobar.service'
LOG_FILE = 'uncertaind_test.txt'
INVVALID_LOG_FILE = 'invalid_uncertaind_test.txt'

_services = Services()
_disks = Disks()

class TestDisk:
    def test_invalid_disk(self):
        assert 404 in _disks.get_disks(device=INVALID_DISK_NAME)

    def test_valid_disk(self):
        partition = _disks.get_partitions()[:1][0][0]
        disk = _disks.get_disks(device=partition)[0]
        dict = {
                'physical': '',
                'device': '',
                'mountpoint': '',
                'fstype': '',
                'total': '',
                'used': '',
                'free': '',
                'percent': '',
                'temperature': ''
            }
        diff = set(dict.keys()) - set(disk.keys())
        assert len(diff) == 0

    def test_invalid_smart(self):
        assert None == _disks.SMART.get_data(device=INVALID_DISK_NAME)

    def test_valid_smart(self):
        device = _disks.SMART.get_devices()[:1]
        smart = _disks.SMART.get_data(device=device)
        assert smart is not None


class TestService:
    def test_add_invalid_service(self):
        assert 404 in _services.add_service(INVALID_SERVICE_NAME)

    def test_remove_invalid_service(self):
        assert 404 in _services.remove_service(INVALID_SERVICE_NAME)

    def test_service_log(self):
        f = open(LOG_FILE, 'w')
        f.write('line1\nline2')
        f.close()

        log_lines = _services.get_service_log(LOG_FILE)

        os.remove(LOG_FILE)
        assert len(log_lines) == 2

    def test_invalid_log_file(self):
        log_lines = _services.get_service_log(INVVALID_LOG_FILE)
        assert len(log_lines) == 0


class TestAPI:
    api_service = Service_API()
    api_disks = Disks_API()

    def test_service_get_invalid(self):
        assert 404 in self.api_service.get(INVALID_SERVICE_NAME)

    def test_service_put_invalid(self):
        assert 404 in self.api_service.put(INVALID_SERVICE_NAME)

    def test_service_delete_invalid(self):
        assert 404 in self.api_service.delete(INVALID_SERVICE_NAME)

    def test_disks_get_invalid(self):
        assert 404 in self.api_disks.get(INVALID_DISK_NAME)

    def test_disks_get_valid(self):
        partition = _disks.get_partitions()[:1][0][0]
        assert 200 in self.api_disks.get(partition)

    def test_disks_get_all(self):
        assert 200 in self.api_disks.get('all')

    def test_disks_get_all_smart(self):
        assert 200 in self.api_disks.get('all+smart')
