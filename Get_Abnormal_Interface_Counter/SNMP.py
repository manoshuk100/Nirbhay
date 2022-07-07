import subprocess

IFINDEXLIST = [0x5000000, 0x1a000000, 0x1a000200, 0x1a000400, 0x1a000600, 0x1a000800, 0x1a000a00, 0x1a000c00,
               0x1a000e00, 0x1a001000, 0x1a001200, 0x1a001400, 0x1a001600, 0x1a001800, 0x1a001a00, 0x1a001c00,
               0x1a001e00, 0x1a002000, 0x1a002200, 0x1a002400, 0x1a002600, 0x1a002800, 0x1a002a00, 0x1a002c00,
               0x1a002e00, 0x1a003000, 0x1a003200, 0x1a003400, 0x1a003600, 0x1a003800, 0x1a003a00, 0x1a003c00,
               0x1a003e00, 0x1a004000, 0x1a004200, 0x1a004400, 0x1a004600, 0x1a004800, 0x1a004a00, 0x1a004c00,
               0x1a004e00, 0x1a005000, 0x1a005200, 0x1a005400, 0x1a005600, 0x1a005800, 0x1a005a00, 0x1a005c00,
               0x1a005e00, 0x1a006000, 0x1a006200, 0x1a006400, 0x1a006600, 0x1a006800, 0x1a006a00]


def snmp_bulkwalk():
    while True:
        for IFINDEX in IFINDEXLIST:
            cmd_1 = "snmpwalk -v2c -c {} {} 1.3.6.1.2.1.31.1.1.1.6.{}".format('public', '10.48.73.136', IFINDEX)
            cmd_2 = "snmpbulkwalk -v2c -c {} {} 1.3.6.1.2.1.31.1.1.1.6.{}".format('public', '10.48.73.136', IFINDEX)
            try:
                output_1 = subprocess.check_output(cmd_1.split(), stderr=subprocess.STDOUT)
                print(output_1)
                output_2 = subprocess.check_output(cmd_2.split(), stderr=subprocess.STDOUT)
                print(output_2)
            except subprocess.CalledProcessError as e:
                print('fail', 'SNMP command "{}" failed, return code: {}, {}'.format(e.cmd, e.returncode, e.output))


if __name__ == '__main__':
    snmp_bulkwalk()
