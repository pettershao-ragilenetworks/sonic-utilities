import os
import sys
import subprocess
from swsscommon.swsscommon import SonicV2Connector
from utilities_common.db import Db

test_path = os.path.dirname(os.path.abspath(__file__))
mock_db_path = os.path.join(test_path, "mirror_input")

modules_path = os.path.dirname(test_path)
scripts_path = os.path.join(modules_path, "acl_loader")

def get_result_and_return_code(cmd):
    return_code = 0
    try:
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        # store only the error, no need for the traceback
        output = e.output.strip().split("\n")[-1]

    print(output)
    return(return_code, output)

class TestShowMirror(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["PATH"] += os.pathsep + scripts_path
        print(os.pathsep + scripts_path)
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def test_mirror_show(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        expected_output = """\
ERSPAN Sessions
Name    Status    SRC IP    DST IP    GRE    DSCP    TTL    Queue    Policer    Monitor Port    SRC Port    Direction
------  --------  --------  --------  -----  ------  -----  -------  ---------  --------------  ----------  -----------

SPAN Sessions
Name       Status    DST Port    SRC Port    Direction    Queue    Policer
---------  --------  ----------  ----------  -----------  -------  ---------
session1   active    Ethernet30  Ethernet40  both
session2   active    Ethernet7   Ethernet8   both
session11  active    Ethernet9   Ethernet10  rx
session15  active    Ethernet2   Ethernet3   tx
"""

        return_code, result = get_result_and_return_code('sudo main.py show session')
        print("return_code: {}".format(return_code))
        print("result = {}".format(result))
        dbconnector.dedicated_dbs = {}
        assert return_code == 0
        assert result == expected_output

