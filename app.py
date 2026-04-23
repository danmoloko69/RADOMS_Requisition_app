# pip install streamlit web3 streamlit-js-eval

import streamlit as st
import os
from web3 import Web3
import streamlit_js_eval
import config

# --- THEME CUSTOMIZATION (Light Green & White) ---
st.set_page_config(page_title=config.APP_NAME, layout="wide")

# Injecting Custom CSS to match the branding
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #2E7D32; /* Forest Green */
    }
    .stButton>button {
        background-color: #C8E6C9; /* Light Green */
        color: #1B5E20;
        border-radius: 20px;
        border: 1px solid #81C784;
    }
    .stSidebar {
        background-color: #F1F8E9; /* Very Pale Green */
    }
    .stMetric {
        background-color: #F1F8E9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BLOCKCHAIN SETUP ---
w3 = Web3(Web3.HTTPProvider(config.SEPOLIA_RPC_URL))
contract_address = w3.to_checksum_address(config.CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=config.CONTRACT_ABI)

def get_request_events(request_id: int):
    events = []
    event_names = [
        "ServiceRequested",
        "TechnicianAssigned",
        "ServiceStarted",
        "ServiceCompleted",
        "ServiceCancelled"
    ]
    for event_name in event_names:
        try:
            event_obj = getattr(contract.events, event_name)
            logs = event_obj().getLogs(fromBlock=0, toBlock='latest')
            for log in logs:
                args = log.get('args', {})
                if args.get('requestId') == request_id:
                    events.append({
                        'event': event_name,
                        'block_number': log.get('blockNumber'),
                        'tx_hash': log.get('transactionHash').hex() if log.get('transactionHash') else None,
                        'args': args
                    })
        except Exception:
            continue
    return sorted(events, key=lambda e: e['block_number'] or 0)

if 'wallet_address' not in st.session_state:
    st.session_state['wallet_address'] = None

if 'customer_portal_step' not in st.session_state:
    st.session_state['customer_portal_step'] = 'login'
if 'customer_logged_in' not in st.session_state:
    st.session_state['customer_logged_in'] = False
if 'customer_email' not in st.session_state:
    st.session_state['customer_email'] = ''
if 'registered_customers' not in st.session_state:
    st.session_state['registered_customers'] = {}

if 'service_provider_logged_in' not in st.session_state:
    st.session_state['service_provider_logged_in'] = False
if 'registered_providers' not in st.session_state:
    st.session_state['registered_providers'] = {}
if 'current_provider_name' not in st.session_state:
    st.session_state['current_provider_name'] = ''
if 'provider_portal_step' not in st.session_state:
    st.session_state['provider_portal_step'] = 'login'

# --- HEADER LOGIC ---
try:
    if os.path.exists(config.LOGO_PATH):
        st.image(config.LOGO_PATH, width=220)
    else:
        st.title(config.APP_NAME)
except Exception:
    st.title(config.APP_NAME)

st.caption(config.TAGLINE)
st.write(config.DESCRIPTION)
st.divider()

# --- SIDEBAR & WALLET ---
with st.sidebar:
    st.header("RADOMS Navigation")
    if st.session_state['wallet_address']:
        st.success(f"Verified Account: {st.session_state['wallet_address'][:6]}...{st.session_state['wallet_address'][-4:]}")
    else:
        if st.button("Connect MetaMask"):
            streamlit_js_eval(js_expressions="window.ethereum.request({method: 'eth_requestAccounts'})", key="connect")
    
    st.divider()
    page = st.radio("Access Level", ["Live Dashboard", "Company Profile", "Customer Portal", "Service Provider", "Supply Chain", "Admin Panel"])

# --- PAGE: COMPANY PROFILE (New Section) ---
if page == "Company Profile":
    st.header("About RADOMS Requisition")
    
    # --- REDESIGNED PROBLEM & SOLUTION SECTIONS ---
    st.markdown("### 🔍 Industry Challenges")
    st.write("The fumigation industry faces critical systemic issues that affect both customers and service providers.")
    
    # Problem metrics in a grid
    prob_col1, prob_col2, prob_col3 = st.columns(3)
    
    with prob_col1:
        st.metric(
            label="Unverified Providers",
            value="High Risk",
            delta="Recurring infestations",
            delta_color="inverse"
        )
        st.caption("Poor quality service leads to customer dissatisfaction")
    
    with prob_col2:
        st.metric(
            label="Supply Chain Gaps", 
            value="No Tracking",
            delta="Quality issues",
            delta_color="inverse"
        )
        st.caption("No system to confirm service completion or track quality")
    
    with prob_col3:
        st.metric(
            label="Pricing Scams",
            value="Hidden Costs",
            delta="Lack of transparency", 
            delta_color="inverse"
        )
        st.caption("Unclear pricing and availability information")
    
    st.divider()
    
    st.markdown("### 🚀 Our Blockchain Solution")
    st.write("RADOMS transforms the industry by shifting from a transactional function to a strategic driver of value.")
    
    # Solution metrics in a grid
    sol_col1, sol_col2, sol_col3 = st.columns(3)
    
    with sol_col1:
        st.metric(
            label="Transparency",
            value="100% Secure",
            delta="Tamper-proof records",
            delta_color="normal"
        )
        st.caption("Every job recorded on the blockchain")
    
    with sol_col2:
        st.metric(
            label="Verified Trust",
            value="Badge System",
            delta="Only verified companies",
            delta_color="normal"
        )
        st.caption("Companies must earn a 'Verified Badge' to take jobs")
    
    with sol_col3:
        st.metric(
            label="Smart Contracts",
            value="Digital Agreements",
            delta="Automated protection",
            delta_color="normal"
        )
        st.caption("Self-executing contracts protect both parties")

    st.divider()
    st.subheader("Real-World Impact")
    st.write("Imagine a family in Alexandra facing a pest infestation. Instead of risking money on informal, unreliable referrals, they use RADOMS to book a trusted company instantly. The entire service lifecycle is recorded on-chain, ensuring accountability and peace of mind.")

# --- PAGE: LIVE DASHBOARD ---
elif page == "Live Dashboard":
    st.header("Network Vital Signs")
    try:
        total_req = contract.functions.requestCount().call()
        fee = contract.functions.COMMISSION_PERCENT().call()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Jobs Logged", total_req)
        c2.metric("Platform Fee", f"{fee}%")
        c3.metric("Network Status", "Active (Sepolia)")

        st.subheader("Permanent Service Ledger")
        if total_req > 0:
            for i in range(total_req, 0, -1):
                data = contract.functions.requests(i).call()
                status = config.STATUS_MAP.get(data[5], "Processing")
                with st.expander(f"Job #{i}: {data[3]} | Status: {status}"):
                    st.write(f"**Location:** {data[4]}")
                    st.write(f"**Customer Address:** {data[1]}")
    except Exception as e:
        st.error(f"Sync failed: {str(e)}")

# --- REMAINING PAGES (Placeholders for core functions) ---
elif page == "Supply Chain":
    st.header("Supply Chain Tracker")
    st.write("Enter a request number to reveal the related blockchain transaction history.")

    request_id = st.number_input("Request Number", min_value=1, step=1)
    if st.button("Reveal Transaction History"):
        try:
            request_data = contract.functions.requests(request_id).call()
            st.markdown(f"**Request ID:** {request_id}")
            st.markdown(f"**Customer:** {request_data[1]}")
            st.markdown(f"**Provider:** {request_data[2]}")
            st.markdown(f"**Pest Type:** {request_data[3]}")
            st.markdown(f"**Service Location:** {request_data[4]}")
            st.markdown(f"**Status:** {config.STATUS_MAP.get(request_data[5], 'Processing')}")
            st.markdown(f"**Created At (Unix):** {request_data[6]}")

            events = get_request_events(request_id)
            if events:
                st.write("### Related Blockchain Events")
                for event in events:
                    with st.expander(f"{event['event']} - Block {event['block_number']}"):
                        if event['tx_hash']:
                            st.write(f"**Transaction Hash:** {event['tx_hash']}")
                        for arg_name, arg_value in event['args'].items():
                            st.write(f"**{arg_name}:** {arg_value}")
            else:
                st.info("No on-chain events found for this request.")
        except Exception as e:
            st.error(f"Unable to load supply chain history: {str(e)}")

elif page == "Customer Portal":
    st.header("Customer Portal")

    if not st.session_state['customer_logged_in']:
        if st.session_state['customer_portal_step'] == 'register':
            st.subheader("Register as a Customer")
            with st.form("register_form"):
                full_name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                create_password = st.text_input("Create Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                contact_number = st.text_input("Contact Number")
                home_address = st.text_area("Home Address")
                if st.form_submit_button("Create Account"):
                    if not email or not create_password or not confirm_password:
                        st.error("Please fill in email, password, and password confirmation.")
                    elif create_password != confirm_password:
                        st.error("Passwords do not match. Please try again.")
                    elif email in st.session_state['registered_customers']:
                        st.warning("This email is already registered. Please login instead.")
                    else:
                        st.session_state['registered_customers'][email] = {
                            'full_name': full_name,
                            'password': create_password,
                            'contact_number': contact_number,
                            'home_address': home_address
                        }
                        st.session_state['customer_logged_in'] = True
                        st.session_state['customer_email'] = email
                        st.session_state['customer_portal_step'] = 'service'
                        st.success("Registration successful. You are now logged in.")
            if st.button("Already a member? Login here"):
                st.session_state['customer_portal_step'] = 'login'
        else:
            st.subheader("Customer Login")
            with st.form("login_form"):
                login_email = st.text_input("Email Address")
                login_password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if login_email in st.session_state['registered_customers']:
                        customer = st.session_state['registered_customers'][login_email]
                        if login_password == customer['password']:
                            st.session_state['customer_logged_in'] = True
                            st.session_state['customer_email'] = login_email
                            st.session_state['customer_portal_step'] = 'service'
                            st.success(f"Welcome back, {customer.get('full_name', login_email)}.")
                        else:
                            st.error("Incorrect password. Please try again.")
                    else:
                        st.warning("No existing account found. Redirecting to registration.")
                        st.session_state['customer_portal_step'] = 'register'
            if st.button("New user? Register here"):
                st.session_state['customer_portal_step'] = 'register'
    else:
        st.success(f"Logged in as {st.session_state['customer_email']}")
        if st.button("Logout"):
            st.session_state['customer_logged_in'] = False
            st.session_state['customer_email'] = ''
            st.session_state['customer_portal_step'] = 'login'

        tab1, tab2 = st.tabs(["Request Service", "Track Service"])

        with tab1:
            st.subheader("Request Fumigation")
            with st.form("req_form"):
                p_type = st.selectbox("Pest Type", ["Cockroaches", "Termites", "Rodents", "Mosquitoes", "Other"])
                desc = st.text_area("Description of the Pest Problem")
                if st.form_submit_button("Submit Request"):
                    # build_and_send_tx logic here
                    st.info("Preparing blockchain request...")

        with tab2:
            st.subheader("Track Your Service")
            if st.session_state['wallet_address']:
                try:
                    total_req = contract.functions.requestCount().call()
                    customer_requests = []
                    for i in range(1, total_req + 1):
                        data = contract.functions.requests(i).call()
                        if data[1].lower() == st.session_state['wallet_address'].lower():
                            customer_requests.append((i, data))

                    if customer_requests:
                        for req_id, data in reversed(customer_requests):
                            status = config.STATUS_MAP.get(data[5], "Processing")
                            with st.expander(f"Job #{req_id}: {data[3]} | Status: {status}"):
                                st.write(f"**Description:** {data[4]}")
                                st.write(f"**Service Provider:** {data[2]}")
                    else:
                        st.info("No service requests found for your account.")
                except Exception as e:
                    st.error(f"Failed to load service status: {str(e)}")
            else:
                st.warning("Please connect your wallet to track your services.")

elif page == "Service Provider":

    st.header("Service Provider Portal")
    
    if not st.session_state['service_provider_logged_in']:
        # Initialize provider portal step
        if 'provider_portal_step' not in st.session_state:
            st.session_state['provider_portal_step'] = 'login'
        
        if st.session_state['provider_portal_step'] == 'login':
            st.subheader("Service Provider Login")
            with st.form("provider_login_form"):
                login_company_name = st.text_input("Company name")
                login_registration_number = st.text_input("Registration number")
                login_password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login"):
                    if login_company_name in st.session_state['registered_providers']:
                        provider = st.session_state['registered_providers'][login_company_name]
                        if (provider.get('registration_number') == login_registration_number and 
                            provider.get('password') == login_password):
                            st.session_state['service_provider_logged_in'] = True
                            st.session_state['current_provider_name'] = login_company_name
                            st.success(f"Welcome back, {login_company_name}!")
                            st.rerun()
                        else:
                            st.error("Invalid registration number or password. Please try again.")
                    else:
                        st.warning("No existing account found. Please register below.")
            
            if st.button("Don't have an account? Register here"):
                st.session_state['provider_portal_step'] = 'register'
                st.rerun()
        
        elif st.session_state['provider_portal_step'] == 'register':
            st.subheader("Service Provider Registration")
            st.write("Please provide your company details for verification and registration.")
            
            with st.form("provider_registration_form"):
                # Registered company name
                company_name = st.text_input("Registered company name")
                
                # Registration number
                registration_number = st.text_input("Registration number (if registered business)")
                
                # Years of operation
                years_operation = st.number_input("Years of operation", min_value=0, step=1)
                
                # Physical address
                physical_address = st.text_area("Physical address")
                
                # Service areas
                service_areas = st.text_input("Service areas (cities/regions covered)")
                
                # Contact details
                contact_phone = st.text_input("Contact phone number")
                contact_email = st.text_input("Contact email")
                
                # Password for account
                create_password = st.text_input("Create Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Submit Registration"):
                    if not company_name or not contact_phone or not contact_email or not create_password:
                        st.error("Please fill in all required fields.")
                    elif create_password != confirm_password:
                        st.error("Passwords do not match. Please try again.")
                    elif company_name in st.session_state['registered_providers']:
                        st.warning("This company name is already registered. Please login instead.")
                    else:
                        st.session_state['registered_providers'][company_name] = {
                            'registration_number': registration_number,
                            'password': create_password,
                            'years_operation': years_operation,
                            'physical_address': physical_address,
                            'service_areas': service_areas,
                            'contact_phone': contact_phone,
                            'contact_email': contact_email
                        }
                        st.session_state['service_provider_logged_in'] = True
                        st.session_state['current_provider_name'] = company_name
                        st.success("Registration successful! You are now logged in.")
                        st.rerun()
            
            if st.button("Already have an account? Login here"):
                st.session_state['provider_portal_step'] = 'login'
                st.rerun()
    else:
        st.subheader("Job Management")
        st.success(f"Logged in as: {st.session_state['current_provider_name']}")
        
        if st.button("Logout"):
            st.session_state['service_provider_logged_in'] = False
            st.session_state['current_provider_name'] = ''
            st.rerun()
        
        # Display allocated jobs for the service provider
        st.write("### Your Allocated Jobs")
        st.divider()
        
        try:
            total_req = contract.functions.requestCount().call()
            provider_jobs = []
            
            # Get all jobs allocated to this provider
            for i in range(1, total_req + 1):
                request_data = contract.functions.requests(i).call()
                # Check if this job is assigned to the current provider
                # request_data[2] is the provider address
                if request_data[2] != "0x0000000000000000000000000000000000000000":  # If provider is assigned
                    # For now, we'll display all assigned jobs
                    # In a production app, you'd match against the provider's wallet address
                    provider_jobs.append((i, request_data))
            
            if provider_jobs:
                # Metrics row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Allocated Jobs", len(provider_jobs))
                with col2:
                    in_progress = sum(1 for _, data in provider_jobs if data[5] == 3)
                    st.metric("In Progress", in_progress)
                with col3:
                    completed = sum(1 for _, data in provider_jobs if data[5] == 4)
                    st.metric("Completed", completed)
                with col4:
                    assigned = sum(1 for _, data in provider_jobs if data[5] == 1)
                    st.metric("Awaiting Start", assigned)
                
                st.divider()
                
                # Filter and display jobs
                job_filter = st.selectbox(
                    "Filter by Status",
                    ["All Jobs", "Assigned", "In Progress", "Completed", "Cancelled"]
                )
                
                # Map filter to status code
                status_filter_map = {
                    "All Jobs": None,
                    "Assigned": 1,
                    "In Progress": 3,
                    "Completed": 4,
                    "Cancelled": 5
                }
                
                selected_status = status_filter_map.get(job_filter)
                
                # Display jobs
                for req_id, data in reversed(provider_jobs):
                    status_code = data[5]
                    
                    # Apply filter
                    if selected_status is not None and status_code != selected_status:
                        continue
                    
                    status = config.STATUS_MAP.get(status_code, "Processing")
                    
                    with st.expander(f"📋 Job #{req_id} - {data[3]} | Status: {status}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Request Details**")
                            st.write(f"**Pest Type:** {data[3]}")
                            st.write(f"**Location:** {data[4]}")
                            st.write(f"**Status:** {status}")
                            st.write(f"**Request ID:** {req_id}")
                        
                        with col2:
                            st.markdown("**Customer Information**")
                            st.write(f"**Customer Address:** {data[1]}")
                            st.write(f"**Created At (Unix):** {data[6]}")
                        
                        st.divider()
                        
                        # Action buttons based on status
                        st_col1, st_col2, st_col3 = st.columns(3)
                        
                        if status_code == 1:  # Assigned - can start service
                            with st_col1:
                                if st.button("✅ Start Service", key=f"start_{req_id}"):
                                    st.success(f"Service for Job #{req_id} has been started!")
                        
                        elif status_code == 3:  # In Progress - can complete service
                            with st_col1:
                                if st.button("🏁 Complete Service", key=f"complete_{req_id}"):
                                    st.success(f"Service for Job #{req_id} has been completed!")
                        
                        # Always allow viewing transaction history
                        with st_col2:
                            if st.button("📊 View History", key=f"history_{req_id}"):
                                events = get_request_events(req_id)
                                if events:
                                    st.write("**Blockchain Events:**")
                                    for event in events:
                                        st.write(f"- {event['event']} (Block {event['block_number']})")
                                else:
                                    st.info("No events recorded yet.")
                        
                        # Cancel button (if not completed or cancelled)
                        if status_code not in [4, 5]:
                            with st_col3:
                                if st.button("❌ Cancel Job", key=f"cancel_{req_id}"):
                                    st.warning(f"Job #{req_id} has been cancelled.")
            else:
                st.info("No jobs allocated to you yet. Check back soon or contact admin for job assignments.")
        except Exception as e:
            st.error(f"Failed to load job assignments: {str(e)}")

elif page == "Admin Panel":
    st.header("System Governance")
    st.write("Use this section to verify SMEs and manage supply chain coordination.")
    
    st.divider()
    
    tab1, tab2 = st.tabs(["Verify SMEs", "Manual Job Assignment"])
    
    with tab1:
        st.subheader("SME Verification")
        st.write("Review and verify service provider registrations.")
        
        if st.session_state['registered_providers']:
            provider_list = list(st.session_state['registered_providers'].keys())
            selected_provider = st.selectbox("Select Service Provider to Verify", provider_list)
            
            if selected_provider:
                provider_data = st.session_state['registered_providers'][selected_provider]
                st.write(f"**Company Name:** {selected_provider}")
                st.write(f"**Registration Number:** {provider_data.get('registration_number', 'N/A')}")
                st.write(f"**Years of Operation:** {provider_data.get('years_operation', 'N/A')}")
                st.write(f"**Physical Address:** {provider_data.get('physical_address', 'N/A')}")
                st.write(f"**Service Areas:** {provider_data.get('service_areas', 'N/A')}")
                st.write(f"**Contact Phone:** {provider_data.get('contact_phone', 'N/A')}")
                st.write(f"**Contact Email:** {provider_data.get('contact_email', 'N/A')}")
                
                if st.button(f"Approve {selected_provider}"):
                    st.success(f"{selected_provider} has been approved as a verified SME.")
        else:
            st.info("No service providers registered yet.")
    
    with tab2:
        st.subheader("Manual Job Assignment")
        st.write("When the system is unable to automatically assign jobs, team members can manually assign them here.")
        
        with st.form("manual_job_assignment"):
            request_id = st.number_input("Request ID", min_value=1, step=1)
            
            if st.session_state['registered_providers']:
                provider_list = list(st.session_state['registered_providers'].keys())
                assigned_provider = st.selectbox("Assign to Service Provider", provider_list)
            else:
                st.warning("No verified service providers available.")
                assigned_provider = None
            
            assignment_notes = st.text_area("Assignment Notes")
            
            if st.form_submit_button("Assign Job"):
                if assigned_provider:
                    st.success(f"Job #{request_id} has been successfully assigned to {assigned_provider}.")
                    st.info(f"Notes: {assignment_notes if assignment_notes else 'No notes provided.'}")
                else:
                    st.error("Please select a service provider to assign the job.")
