# Test Category:
# Security Configuration Test

# Requirements Covered:
# NFR1.1
# NFR1.3

def test_backend_communication_uses_internal_vlan(app_config):
    """
    Validates that the backend configuration exclusively routes
    database and email traffic through the internal VLAN to 
    protect against external interception.
    
    Semantic focus:
    prevent ("förhindra")
    interception ("avlyssning")
    protection ("skydd")
    """
    
    db_host = app_config.get("DATABASE_HOST")
    email_host = app_config.get("EMAIL_HOST")
    
    # The internal VLAN is defined as 192.168.2.0/24
    expected_subnet_prefix = "192.168.2."
    
    # Validate DB routing (VM 2)
    assert db_host.startswith(expected_subnet_prefix), \
        f"Security violation: DB traffic routed outside VLAN ({db_host})"
    assert db_host == "192.168.2.3"
    
    # Validate Email routing (VM 3 internal IP constraint)
    # Assuming the app config strictly maps to the internal IP for VM 3
    assert email_host.startswith(expected_subnet_prefix), \
        f"Security violation: Email traffic routed outside VLAN ({email_host})"