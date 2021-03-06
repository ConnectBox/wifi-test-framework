"""generate a script that can be used to run a long-running test"""

REPEAT_COUNT = 3
TARGETS = ["neo-hatgen2", "neo-hatgen3"]
EXTRA_RUN_DESC = "@15ft-internal-control"
INVENTORIES = [
    "test_inventories/20c20s-360p",
    "test_inventories/16c16s-480p",
]

TARGET_OVERRIDES = {
    "neo": [
        "-e wifi_network_under_test='neo.connectbox'",
        "-e test_server_hostname='neo.connectbox'",
    ],
    "neo-hatgen2": [
        "-e wifi_network_under_test='neo-hatgen2.connectbox'",
        "-e test_server_hostname='connectbox'",
    ],
    "neo-hatgen3": [
        "-e wifi_network_under_test='neo-hatgen3.connectbox'",
        "-e test_server_hostname='connectbox'",
    ],
    "pilot1": [
        "-e wifi_network_under_test='pilot1.connectbox'",
        "-e test_server_hostname='pilot1.connectbox'",
    ],
    "pilot2": [
        "-e wifi_network_under_test='pilot2.connectbox'",
        "-e test_server_hostname='pilot2.connectbox'",
    ],
    "rpi3": [
        "-e wifi_network_under_test='rpi3.connectbox'",
        "-e test_server_hostname='rpi3.connectbox'",
    ],
    "rpi0w": [
        "-e wifi_network_under_test='rpi0w.connectbox'",
        "-e test_server_hostname='rpi0w.connectbox'",
    ],
    "tp3040": [
        "-e wifi_network_under_test='tp3040.connectbox'",
        "-e test_server_hostname='tp3040.connectbox'",
        "-e test_server_ip='192.168.1.1",
        "-e test_file_path='Shared/throughput-test/10MB.bin",
    ],
}

print('# Generated script follows')
print('group_datestamp=$(date +%y%m%d%H%M);')
print('echo "Setting up clients"')
print('sort -u %s > all_clients' % (" ".join(INVENTORIES),))
print('ansible-playbook -i all_clients run.yml --tags=setup-system')
print('rm all_clients')

for c in range(REPEAT_COUNT):
    print('echo "Interation start: $(date)"')
    for i in INVENTORIES:
        for t in TARGETS:
            group_id = "-".join(filter(None, [t, i, EXTRA_RUN_DESC]))
            print('# Starting %s' % (group_id,))
            print('ansible-playbook -i %s run.yml --tags=task_execution '
                  '-e test_group_id=%s-${group_datestamp} %s' %
                  (i, group_id, " ".join(TARGET_OVERRIDES[t])))
