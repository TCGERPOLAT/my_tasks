import pytest
import task_24_2b
from netmiko.cisco.cisco_ios import CiscoIosSSH
import sys

sys.path.append("..")

from pyneng_common_functions import check_class_exists, check_attr_or_method

# Checking that the test is called via pytest ... and not python ...
from _pytest.assertion.rewrite import AssertionRewritingHook

if not isinstance(__loader__, AssertionRewritingHook):
    print(f"Tests should be called using this expression:\npytest {__file__}\n\n")


def test_class_created():
    check_class_exists(task_24_2b, "MyNetmiko")


def test_class_inheritance(first_router_from_devices_yaml):
    r1 = task_24_2b.MyNetmiko(**first_router_from_devices_yaml)
    r1.disconnect()
    assert isinstance(r1, CiscoIosSSH), "MyNetmiko class must inherit from CiscoIosSSH"
    check_attr_or_method(r1, method="send_command")
    check_attr_or_method(r1, method="_check_error_in_command")


@pytest.mark.parametrize(
    "error,command",
    [
        ("Invalid input detected", "logging 0255.255.1"),
        ("Incomplete command", "lo"),
        ("Ambiguous command", "a"),
    ],
)
def test_errors(first_router_from_devices_yaml, command, error):
    r1 = task_24_2b.MyNetmiko(**first_router_from_devices_yaml)
    with pytest.raises(Exception) as excinfo:
        return_value = r1.send_config_set(command)
        r1.disconnect()
    assert error in str(
        excinfo
    ), "send_config_commands method should throw an exception when the command is executed with an error"
