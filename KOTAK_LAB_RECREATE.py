from netmiko import ConnectHandler
import time


# Function to execute commands on a switch
def execute_commands(device_info, commands, prompt_pattern, iterations):
    try:
        # Connect to the switch
        with ConnectHandler(**device_info) as ssh:
            print(f'Connected to {device_info["ip"]}')
            print(f'Started to execute the commands...')

            for _ in range(iterations):
                # Execute commands
                for command in commands:
                    ssh.send_command(command, expect_string=prompt_pattern)
                    # print(f"Command: {command} executed")

    except Exception as e:
        print(f"Error: {str(e)}")


# Common login details
login_info = {
    "device_type": "cisco_nxos",
    "username": "admin",
    "password": "cisco!123",
}

# Switch details
switches = [
    {"ip": "10.122.163.56"},
    {"ip": "10.122.163.58"},
    {"ip": "10.122.163.120"},
    {"ip": "10.122.163.50"},
]

# Commands to execute
global_commands = [
    "config ; spanning-tree port type edge default",
    "config ; spanning-tree port type edge bpduguard default",
    "config ; spanning-tree loopguard default",
    "config ; no spanning-tree port type edge default",
    "config ; no spanning-tree port type edge bpduguard default",
    "config ; no spanning-tree loopguard default",
]

interface_commands = [
    "config ; interface po10 ; spanning-tree port type edge default",
    "config ; interface po10 ; spanning-tree port type edge bpduguard default",
    "config ; interface po10 ; spanning-tree loopguard default",
    "config ; interface po10 ; no spanning-tree port type edge default",
    "config ; interface po10 ; no spanning-tree port type edge bpduguard default",
    "config ; interface po10 ; no spanning-tree loopguard default",
]

stp_vlan_priority_commands = [
    "config ; spanning-tree vlan 1-3967 priority 12288",
    "config ; spanning-tree vlan 1-3967 priority 4096",
]

stp_vlan_priority_commands_56 = [
    "config ; spanning-tree vlan 1-3967 priority 8192",
    "config ; spanning-tree vlan 1-3967 priority 4096",
]

mst_commands_7K = [
    "config ; spanning-tree mode mst",
    "spanning-tree mst configuration",
    "name MST_INSTANCE_A",
    "revision 1",
    "instance 1 vlan 1-3967",
    "exit",
    "spanning-tree mst 1 priority 4096",
    "exit",
    "config ; interface po10 ; spanning-tree mst 1 priority 4096",
]

mst_commands_9K = [
    "config ; spanning-tree mode mst",
    "spanning-tree mst configuration",
    "name MST_INSTANCE_B",
    "revision 1",
    "instance 1 vlan 1-3967",
    "exit",
    "spanning-tree mst 1 priority 4096",
    "exit",
    "config ; interface po10 ; spanning-tree mst 1 priority 4096",
]

mst_no_commands_7K = [
    "config ; no spanning-tree mst 1 priority",
    "no spanning-tree mst configuration",
    "no spanning-tree mode mst",
    "config ; interface po10 ; no spanning-tree mst 1 priority 4096"
]

mst_no_commands_9K = [
    "config ; no spanning-tree mst 1 priority",
    "no spanning-tree mst configuration",
    "no spanning-tree mode mst",
    "config ; interface po10 ; no spanning-tree mst 1 priority 4096"
]

# Number of iterations
iterations = 50


def main_1():
    for switch in switches:
        if switch["ip"] == "10.122.163.56" or switch["ip"] == "10.122.163.58":
            execute_commands({**login_info, **switch}, global_commands, " ", iterations)
            execute_commands({**login_info, **switch}, interface_commands, " ", iterations)
            execute_commands({**login_info, **switch}, stp_vlan_priority_commands, " ", iterations)
        if switch["ip"] == "10.122.163.56":
            execute_commands({**login_info, **switch}, stp_vlan_priority_commands_56, " ", iterations)


def main_2():
    for i in range(1, iterations + 1):
        # Configure "10.122.163.56" and "10.122.163.58" with MST instance A
        execute_commands({**login_info, **switches[0]}, mst_commands_7K, " ", i)
        execute_commands({**login_info, **switches[1]}, mst_commands_7K, " ", i)

        # Configure "10.122.163.120" and "10.122.163.50" with MST instance B
        execute_commands({**login_info, **switches[2]}, mst_commands_9K, " ", i)
        execute_commands({**login_info, **switches[3]}, mst_commands_9K, " ", i)

        time.sleep(5)

        # Unconfigure "10.122.163.56" and "10.122.163.58" with MST instance A
        execute_commands({**login_info, **switches[0]}, mst_no_commands_7K, " ", i)
        execute_commands({**login_info, **switches[1]}, mst_no_commands_7K, " ", i)

        # Unconfigure "10.122.163.120" and "10.122.163.50" with MST instance B
        execute_commands({**login_info, **switches[2]}, mst_no_commands_9K, " ", i)
        execute_commands({**login_info, **switches[3]}, mst_no_commands_9K, " ", i)
        time.sleep(3)  # Sleep for 20 seconds before the next iteration


if __name__ == '__main__':
    main_1()
    main_2()
