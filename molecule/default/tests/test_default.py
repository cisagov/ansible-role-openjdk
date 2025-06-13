"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os
import pathlib

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


@pytest.mark.parametrize(
    "d, tool",
    [
        (
            "bin",
            "jaotc",
        ),
        (
            "bin",
            "jar",
        ),
        (
            "bin",
            "jarsigner",
        ),
        (
            "bin",
            "java",
        ),
        (
            "bin",
            "javac",
        ),
        (
            "bin",
            "javadoc",
        ),
        (
            "bin",
            "javap",
        ),
        (
            "bin",
            "jcmd",
        ),
        (
            "bin",
            "jconsole",
        ),
        (
            "bin",
            "jdb",
        ),
        (
            "bin",
            "jdeprscan",
        ),
        (
            "bin",
            "jdeps",
        ),
        (
            "lib",
            "jexec",
        ),
        (
            "bin",
            "jfr",
        ),
        (
            "bin",
            "jhsdb",
        ),
        (
            "bin",
            "jimage",
        ),
        (
            "bin",
            "jinfo",
        ),
        (
            "bin",
            "jjs",
        ),
        (
            "bin",
            "jlink",
        ),
        (
            "bin",
            "jmap",
        ),
        (
            "bin",
            "jmod",
        ),
        (
            "bin",
            "jps",
        ),
        (
            "bin",
            "jrunscript",
        ),
        (
            "bin",
            "jshell",
        ),
        (
            "bin",
            "jstack",
        ),
        (
            "bin",
            "jstat",
        ),
        (
            "bin",
            "jstatd",
        ),
        (
            "bin",
            "keytool",
        ),
        (
            "bin",
            "pack200",
        ),
        (
            "bin",
            "rmic",
        ),
        (
            "bin",
            "rmid",
        ),
        (
            "bin",
            "rmiregistry",
        ),
        (
            "bin",
            "serialver",
        ),
        (
            "bin",
            "unpack200",
        ),
    ],
)
def test_alternatives(host, d, tool):
    """Test that the alternatives are configured as expected for Kali instances."""
    distribution = host.system_info.distribution
    if distribution == "kali":
        arch = host.system_info.arch
        if arch == "x86_64":
            arch_alias = "amd64"
        elif arch == "aarch64":
            arch_alias = "arm64"
        else:
            assert False, f"Unknown architecture {arch}"

        alternative_path = str(pathlib.PurePath("/etc/alternatives", tool))
        f = host.file(alternative_path)
        assert f.exists
        assert f.is_symlink
        assert f.linked_to == str(
            pathlib.PurePath(f"/usr/lib/jvm/java-11-openjdk-{arch_alias}", d, tool)
        )


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if distribution in ["debian"]:
        if codename in ["buster"]:
            assert host.package("openjdk-11-jdk").is_installed
        elif codename in ["bullseye", "bookworm"]:
            assert host.package("openjdk-17-jdk").is_installed
        else:
            assert host.package("openjdk-21-jdk").is_installed
    elif distribution in ["kali", "ubuntu"]:
        assert host.package("openjdk-11-jdk").is_installed
    elif distribution in ["fedora"]:
        assert host.package("java-11-openjdk-devel").is_installed
    elif distribution in ["amzn"]:
        assert host.package("java-11-amazon-corretto-devel").is_installed
    else:
        assert False, f"Unknown distribution: {distribution}"
