from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint


mgmt = ManagementRoot("192.168.109.130", "admin", "pass")


######### version check

        self.s = self.mgmt._meta_data['bigip']._meta_data['icr_session']
        self.tmos_version = self._tmos_version()
        if LooseVersion(self.tmos_version) < LooseVersion('12.1.0'):
            raise Exception,"This has only been tested on 12.1."
    def _tmos_version(self):
        connect = self.mgmt._meta_data['bigip']._meta_data['icr_session']
        base_uri = self.mgmt._meta_data['uri'] + 'tm/sys/'
        response = connect.get(base_uri)
        ver = response.json()

        version = parse_qs(urlparse(ver['selfLink']).query)['ver'][0]
        return version