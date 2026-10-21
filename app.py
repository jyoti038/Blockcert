
import streamlit as st
import hashlib
import json
from datetime import datetime

st.set_page_config(
    page_title="BlockCert",
    page_icon="🔗"
)

# Generate SHA-256 hash for a block
def calculate_hash(block):
    block_data = {
        key: value
        for key, value in block.items()
        if key != "hash"
    }
    text = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()


# Create a new blockchain block
def create_block(index, name, roll, course, previous_hash):
    block = {
        "index": index,
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "roll": roll,
        "course": course,
        "previous_hash": previous_hash
    }
    block["hash"] = calculate_hash(block)
    return block


# Validate all blocks and their hash links
def validate_chain(chain):
    for i, block in enumerate(chain):
        if calculate_hash(block) != block["hash"]:
            return False

        if i == 0:
            if block["previous_hash"] != "0":
                return False
        elif block["previous_hash"] != chain[i - 1]["hash"]:
            return False

    return True


# Create the first block
if "chain" not in st.session_state:
    st.session_state.chain = [
        create_block(
            0, "Genesis Block", "0", "Blockchain", "0"
        )
    ]


# Website heading
st.title("🔗 BlockCert")
st.write("Blockchain-Based Certificate Verification System")
st.caption("A simple educational blockchain project")

st.divider()

# Add certificate
st.header("1. Add Student Certificate")

with st.form("certificate_form"):
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    course = st.text_input("Course Name")

    submitted = st.form_submit_button("Add Certificate")

if submitted:
    if not name.strip() or not roll.strip() or not course.strip():
        st.error("Please fill in all fields.")
    elif any(
        b["roll"] == roll.strip()
        for b in st.session_state.chain[1:]
    ):
        st.error("This roll number already exists.")
    else:
        previous_hash = st.session_state.chain[-1]["hash"]

        block = create_block(
            len(st.session_state.chain),
            name.strip(),
            roll.strip(),
            course.strip(),
            previous_hash
        )

        st.session_state.chain.append(block)
        st.success("Certificate added to blockchain!")


st.divider()

# Verify certificate
st.header("2. Verify Certificate")

search_roll = st.text_input("Enter Roll Number")

if st.button("Verify Certificate"):
    matches = [
        block for block in st.session_state.chain[1:]
        if block["roll"] == search_roll.strip()
    ]

    if matches:
        st.success("Certificate record found!")
        st.json(matches[0])
    else:
        st.error("Certificate not found.")


st.divider()

# Display blockchain
st.header("3. Blockchain Records")

for block in st.session_state.chain:
    with st.expander(f"Block {block['index']}"):
        st.json(block)


st.divider()

# Validate blockchain
st.header("4. Validate Blockchain")

if st.button("Validate Chain"):
    if validate_chain(st.session_state.chain):
        st.success("Blockchain is valid! All hashes match.")
    else:
        st.error("Tampering detected! Blockchain is invalid.")

st.caption(
    "Educational simulation using Python and SHA-256 hashing."
)
