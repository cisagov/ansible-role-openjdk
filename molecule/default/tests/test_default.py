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


@pytest.mark.parametrize("pkg", ["openjdk-11-jdk"])
def test_debian_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if distribution == "debian" and codename != "stretch":
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["openjdk-8-jdk"])
def test_debian_9_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if distribution == "debian" and codename == "stretch":
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["openjdk-8-jdk"])
def test_ubuntu_xenial_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if distribution == "ubuntu" and codename == "xenial":
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["java-11-openjdk-devel"])
def test_redhat_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution == "fedora":
        assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["java-1.8.0-openjdk-devel"])
def test_amazon_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution == "amzn":
        assert host.package(pkg).is_installed
