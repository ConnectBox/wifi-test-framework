REPEAT_COUNT = 5
TARGETS = ["pilot1", "pilot2"]
EXTRA_RUN_DESC = "@20ft"
INVENTORIES = [
    "test_inventories/4c4s-480p",
]

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

print('# Generated script follows')
print('group_datestamp=$(date +%y%m%d%H%M);')
for c in range(REPEAT_COUNT):
    print('echo "Interation start: $(date)"')
    for i in INVENTORIES:
        for t in TARGETS:
            group_id = "-".join(filter(None, [t, i, EXTRA_RUN_DESC]))
            print('# Starting %s' % (group_id,))
            print('ansible-playbook -i %s run.yml '
                  '-e test_group_id=%s-${group_datestamp} %s' %
                  (i, group_id, " ".join(TARGET_OVERRIDES[t])))
