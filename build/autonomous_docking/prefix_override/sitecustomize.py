import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ivanovaml/subsea_robotics_workspace/install/autonomous_docking'
