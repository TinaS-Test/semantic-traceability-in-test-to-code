# ============================================================
# Test Category  : Smoke / Infrastructure
# Requirement(s) : Doc 1 – Chapter 1.1 (Architecture & Infrastructure)
#                  NFR1.3 (DB must reject external connections)
# ============================================================

import socket
import pytest

# Renamed from generic "hosts" to "vm_network_endpoints" for traceability.
# Each tuple: (host, port, human-readable label)
VM_NETWORK_ENDPOINTS = [
    ("tina.ethernettrip.com",  443,  "VM1 – App Server (HTTPS)"),
    ("192.168.2.3",            5432, "VM2 – PostgreSQL (internal)"),
    ("mail.ethernettrip.com",  25,   "VM3 – Postfix SMTP"),
    ("gitlab.ethernettrip.com", 443, "VM4 – GitLab (HTTPS)"),
]

DB_PUBLIC_IP = "46.62.214.236"  # VM2 public IP — must not expose port 5432
DB_PORT = 5432
SOCKET_TIMEOUT_SECONDS = 3


def _check_port(host: str, port: int) -> int:
    """Returns 0 if connection succeeds, non-zero if refused/unreachable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCKET_TIMEOUT_SECONDS)
    result = sock.connect_ex((host, port))
    sock.close()
    return result


@pytest.mark.parametrize("host, port, label", VM_NETWORK_ENDPOINTS)
def test_vm_endpoint_reachability(host: str, port: int, label: str):
    """
    Verifies each VM in the architecture is reachable on its expected port.
    Fails fast — if this test fails, all integration tests are expected to fail too.
    """
    result = _check_port(host, port)
    assert result == 0, f"Unreachable endpoint: {label} ({host}:{port})"


def test_db_rejects_external_connections():
    """
    NFR1.3: The database must not accept connections from outside 192.168.2.0/24.
    This test attempts a connection to the DB's public IP — it must be refused.
    """
    result = _check_port(DB_PUBLIC_IP, DB_PORT)
    assert result != 0, (
        f"SECURITY VIOLATION: DB at {DB_PUBLIC_IP} accepted an external connection on port {DB_PORT}."
    )