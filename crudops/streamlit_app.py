# streamlit_app.py
import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/api/items/'

def list_items():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []

def create_item(name, desc, qty):
    payload = {"name": name, "description": desc, "quantity": qty}
    response = requests.post(API_URL, json=payload)
    return response.status_code == 201

def update_item(item_id, name, desc, qty):
    payload = {"name": name, "description": desc, "quantity": qty}
    response = requests.put(f"{API_URL}{item_id}/", json=payload)
    return response.status_code == 200

def delete_item(item_id):
    response = requests.delete(f"{API_URL}{item_id}/")
    return response.status_code == 204

st.title("Django CRUD with Streamlit")

# CREATE
st.subheader("Create New Item")
name = st.text_input("Name")
desc = st.text_area("Description")
qty = st.number_input("Quantity", min_value=0, step=1)

if st.button("Add Item"):
    if create_item(name, desc, qty):
        st.success("Item created!")

# READ
st.subheader("All Items")
items = list_items()
for item in items:
    st.write(f"**{item['name']}** - {item['description']} (Qty: {item['quantity']})")

# UPDATE / DELETE (optional UI here)
st.subheader("Update or Delete an Item")
selected_id = st.selectbox("Select Item by ID", [item["id"] for item in items])
selected_item = next((item for item in items if item["id"] == selected_id), None)

if selected_item:
    new_name = st.text_input("Edit Name", value=selected_item["name"])
    new_desc = st.text_area("Edit Description", value=selected_item["description"])
    new_qty = st.number_input("Edit Quantity", min_value=0, value=selected_item["quantity"])

    if st.button("Update"):
        if update_item(selected_id, new_name, new_desc, new_qty):
            st.success("Item updated!")

    if st.button("Delete"):
        if delete_item(selected_id):
            st.success("Item deleted!")

