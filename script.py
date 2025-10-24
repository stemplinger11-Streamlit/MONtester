
# Erstelle die Streamlit App als Single Python File
streamlit_app_code = '''import streamlit as st
import re

# Page Configuration
st.set_page_config(
    page_title="SNMP Monitoring Tester",
    page_icon="🔍",
    layout="centered"
)

# Title and Description
st.title("🔍 Monitoring Tester")
st.markdown("**Generate SNMP Configuration and Test Commands**")
st.divider()

# Helper Functions
def validate_ip(ip):
    """Validate IP address format"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def validate_password(password):
    """Validate password - no special characters: +, !, /, ", ?, &"""
    forbidden_chars = ['+', '!', '/', '"', '?', '&']
    for char in forbidden_chars:
        if char in password:
            return False, char
    return True, None

def generate_commands(snmpv3_user, auth_pw, priv_pw, zone, ip_range):
    """Generate the two commands"""
    cmd1 = f"snmp-server user {snmpv3_user} v3 sha1 plain {auth_pw} {priv_pw}"
    cmd2 = f"test_snmp --snmpv3user {snmpv3_user} --snmpv3pwd '{auth_pw}' --snmpv3privauth '{priv_pw}' --zone {zone} --iprange {ip_range}"
    return cmd1, cmd2

# Input Section
st.subheader("📝 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    snmpv3_user = st.text_input(
        "SNMPv3 Username",
        value="",
        placeholder="e.g., snmp4ise",
        help="Enter the SNMPv3 username"
    )
    
    auth_pw = st.text_input(
        "Auth Password",
        value="",
        placeholder="e.g., Auth-PW",
        help="Authentication password (no +, !, /, \", ?, & allowed)"
    )

with col2:
    priv_pw = st.text_input(
        "Privacy Password",
        value="",
        placeholder="e.g., Priv-PW",
        help="Privacy password (no +, !, /, \", ?, & allowed)"
    )
    
    zone = st.text_input(
        "Zone",
        value="",
        placeholder="e.g., XXX",
        help="Zone identifier"
    )

ip_range = st.text_input(
    "IP Range",
    value="",
    placeholder="e.g., 100.100.100.100",
    help="IP address or range"
)

st.divider()

# Buttons
col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])

with col_btn1:
    generate_btn = st.button("🚀 Generate Commands", type="primary", use_container_width=True)

with col_btn2:
    example_btn = st.button("📋 Load Example", use_container_width=True)

with col_btn3:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

# Load Example Data
if example_btn:
    st.session_state.snmpv3_user = "snmp4ise"
    st.session_state.auth_pw = "Auth-PW"
    st.session_state.priv_pw = "Priv-PW"
    st.session_state.zone = "XXX"
    st.session_state.ip_range = "100.100.100.100"
    st.rerun()

# Clear All Fields
if clear_btn:
    for key in ['snmpv3_user', 'auth_pw', 'priv_pw', 'zone', 'ip_range']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Apply session state values
if 'snmpv3_user' in st.session_state:
    snmpv3_user = st.session_state.snmpv3_user
if 'auth_pw' in st.session_state:
    auth_pw = st.session_state.auth_pw
if 'priv_pw' in st.session_state:
    priv_pw = st.session_state.priv_pw
if 'zone' in st.session_state:
    zone = st.session_state.zone
if 'ip_range' in st.session_state:
    ip_range = st.session_state.ip_range

# Generate Commands
if generate_btn:
    # Validation
    errors = []
    
    if not snmpv3_user:
        errors.append("❌ SNMPv3 Username is required")
    
    if not auth_pw:
        errors.append("❌ Auth Password is required")
    else:
        valid, char = validate_password(auth_pw)
        if not valid:
            errors.append(f"❌ Auth Password contains forbidden character: '{char}'")
    
    if not priv_pw:
        errors.append("❌ Privacy Password is required")
    else:
        valid, char = validate_password(priv_pw)
        if not valid:
            errors.append(f"❌ Privacy Password contains forbidden character: '{char}'")
    
    if not zone:
        errors.append("❌ Zone is required")
    
    if not ip_range:
        errors.append("❌ IP Range is required")
    elif not validate_ip(ip_range):
        errors.append("❌ Invalid IP address format")
    
    # Display Errors or Commands
    if errors:
        st.error("### ⚠️ Validation Errors")
        for error in errors:
            st.write(error)
    else:
        # Generate Commands
        cmd1, cmd2 = generate_commands(snmpv3_user, auth_pw, priv_pw, zone, ip_range)
        
        st.success("✅ Commands generated successfully!")
        st.divider()
        
        # Command 1: SNMP Server Configuration
        st.subheader("🔧 Command 1: SNMP Server Configuration")
        st.code(cmd1, language="bash")
        
        st.divider()
        
        # Command 2: SNMP Test
        st.subheader("🧪 Command 2: SNMP Test")
        st.code(cmd2, language="bash")
        
        st.divider()
        
        # Copy Instructions
        st.info("💡 **Tip:** Click on the commands above to copy them to your clipboard!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Monitoring Tester v1.0 | Built with Streamlit</p>
    <p>Forbidden password characters: + ! / " ? &</p>
</div>
""", unsafe_allow_html=True)
'''

# Speichere die App
with open('monitoring_tester.py', 'w', encoding='utf-8') as f:
    f.write(streamlit_app_code)

print("✅ Streamlit App erfolgreich erstellt: monitoring_tester.py")
print("\n📝 App-Features:")
print("  - 5 Input-Felder (SNMPv3 User, Auth-PW, Priv-PW, Zone, IP-Range)")
print("  - Validierung aller Eingaben")
print("  - Passwort-Validierung (keine +, !, /, \", ?, &)")
print("  - IP-Adress-Validierung")
print("  - 'Load Example' Button mit Beispieldaten")
print("  - 'Clear' Button zum Zurücksetzen")
print("  - Separate Code-Boxen für beide Commands mit Copy-Funktion")
print("\n🚀 Deployment:")
print("  1. File auf GitHub hochladen")
print("  2. Streamlit Community Cloud verbinden")
print("  3. monitoring_tester.py als Main File wählen")
print("\n📦 Requirements: Nur Streamlit (wird automatisch installiert)")
