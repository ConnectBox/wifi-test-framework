
#REPEAT_COUNT = 20
#TARGETS = ["neo", "rpi3"]
REPEAT_COUNT = 2
TARGETS = ["tp3040"]
EXTRA_RUN_DESC = ""

TARGET_OVERRIDES = {
    "neo": [
        "-e wifi_network_under_test='neo.connectbox'",
        "-e test_server_hostname='neo.connectbox'",
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
INVENTORIES = [
    "test_inventories/1c8s",
    "test_inventories/2c8s",
    "test_inventories/3c8s",
    "test_inventories/4c8s",
    "test_inventories/5c8s",
    "test_inventories/6c8s",
    "test_inventories/7c8s",
    "test_inventories/8c8s",
    "test_inventories/9c9s",
    "test_inventories/10c10s",
    "test_inventories/12c12s",
    "test_inventories/14c14s",
    "test_inventories/21c21s",
]

print('# Generated script follows')
for c in range(REPEAT_COUNT):
    print('echo "Interation start: $(date)"')
    for i in INVENTORIES:
        for t in TARGETS:
            group_id = "-".join(filter(None, [t, i, EXTRA_RUN_DESC]))
            print('# Starting %s' % (group_id,))
            print('ansible-playbook -i %s run.yml -e test_group_id=%s %s' %
                  (i, group_id, " ".join(TARGET_OVERRIDES[t])))
