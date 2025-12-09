"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "d",
    [
        "/usr/share/man/man1",
        "/usr/share/man/man2",
        "/usr/share/man/man3",
        "/usr/share/man/man4",
        "/usr/share/man/man5",
        "/usr/share/man/man6",
        "/usr/share/man/man7",
        "/usr/share/man/man8",
    ],
)
def test_man_dirs(host, d):
    """Test that the expected directories are present for Debian instances."""
    distribution = host.system_info.distribution
    if distribution == "debian":
        assert host.file(d).exists


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if distribution in ["debian", "kali"]:
        if codename in ["buster"]:
            assert host.package("openjdk-11-jdk").is_installed
        elif codename in ["bullseye", "bookworm"]:
            assert host.package("openjdk-17-jdk").is_installed
        else:
            assert host.package("openjdk-21-jdk").is_installed
    elif distribution in ["ubuntu"]:
        assert host.package("openjdk-17-jdk").is_installed
    elif distribution in ["fedora"]:
        assert host.package("java-21-openjdk-devel").is_installed
    elif distribution in ["amzn"]:
        assert host.package("java-17-amazon-corretto-devel").is_installed
    else:
        assert False, f"Unknown distribution: {distribution}"
