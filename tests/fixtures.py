import os
from nose import SkipTest

def real_winrm_service():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.isfile(config_path):
        # TODO consider replace json with yaml for integration test settings
        # TODO json module does not exists in Python 2.5 library and does not support comments
        import json
        settings = json.load(open(config_path))

        from winrm_service import WinRMWebService
        winrm = WinRMWebService(**settings)
        return winrm
    else:
        raise SkipTest('config.json was not found. Integration tests will be skipped')