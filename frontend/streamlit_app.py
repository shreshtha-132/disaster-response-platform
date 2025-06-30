import streamlit as st
import requests

BACKEND_URL="https://disaster-response-platform-backend-k4qf.onrender.com"
st.set_page_config(page_title="Disaster Response Platform", layout="centered")
st.title("🌪️ Disaster Response Platform")

st.sidebar.header("📍 Navigation")
section = st.sidebar.selectbox("Choose Action",[
    "Report Disaster",
    "Get All Disasters",
    "Update Disaster",
    "Delete Disaster",
    "Add Resource",
    "Resources by Disaster ID",
    "Resources by Location",
    "Social Media Posts",
    "Official Updates",
    "Verify Disaster Image"
])

if section == "Report Disaster":
    st.subheader("🧨 Report a New Disaster")

    title = st.text_input("Disaster Title")
    description = st.text_area("Describe the situation")
    tags = st.text_input("Tags (comma-separated)").split(",")
    owner_id = st.text_input("Owner ID")

    if st.button("Submit Report"):
        data = {
            "title": title,
            "description": description,
            "tags": tags,
            "owner_id": owner_id
        }
        res = requests.post(f"{BACKEND_URL}/disasters", json=data)
        st.success(res.json())

elif section == "Get All Disasters":
    st.subheader("📄 List of All Disasters")
    res = requests.get(f"{BACKEND_URL}/disasters")
    if res.ok:
        for d in res.json()["disasters"]:
            st.json(d)

elif section == "Update Disaster":
    st.subheader("🛠 Update Existing Disaster")
    disaster_id = st.text_input("Disaster ID (UUID)")
    new_desc = st.text_area("New Description")
    owner_id = st.text_input("Updater Owner ID")

    if st.button("Update"):
        data = {
            "description": new_desc,
            "owner_id": owner_id
        }
        res = requests.put(f"{BACKEND_URL}/disasters/{disaster_id}", json=data)
        st.success(res.json())

elif section == "Delete Disaster":
    st.subheader("❌ Delete Disaster by ID")
    disaster_id = st.text_input("Disaster ID (UUID)")
    if st.button("Delete Disaster"):
        res = requests.delete(f"{BACKEND_URL}/disasters/{disaster_id}")
        st.warning(res.json())

elif section == "Add Resource":
    st.subheader("➕ Add Resource to Disaster")

    disaster_id = st.text_input("Disaster ID")
    name = st.text_input("Resource Name")
    location_name = st.text_input("Location Name")
    type_ = st.text_input("Resource Type")

    if st.button("Add Resource"):
        data = {
            "disaster_id": disaster_id,
            "name": name,
            "location_name": location_name,
            "type": type_
        }
        res = requests.post(f"{BACKEND_URL}/resources", json=data)
        st.success(res.json())


elif section == "Resources by Disaster ID":
    st.subheader("🔎 Resources Linked to a Disaster")
    disaster_id = st.text_input("Disaster ID")
    if st.button("Fetch Resources"):
        res = requests.get(f"{BACKEND_URL}/resources/{disaster_id}/resources")
        st.json(res.json())


elif section == "Resources by Location":
    st.subheader("🌍 Find Resources Nearby")
    location_name = st.text_input("Enter Location Name")
    if st.button("Find Resources"):
        res = requests.get(f"{BACKEND_URL}/resources/{location_name}/resources")
        st.json(res.json())


elif section == "Social Media Posts":
    st.subheader("📱 Social Media Posts")
    res = requests.get(f"{BACKEND_URL}/social-media/posts")
    st.json(res.json())


elif section == "Official Updates":
    st.subheader("📰 Official Updates")
    res = requests.get(f"{BACKEND_URL}/official-updates")
    st.json(res.json())


elif section == "Verify Disaster Image":
    st.subheader("🖼 Verify Image")
    image_url = st.text_input("Enter Image URL")

    if st.button("Verify"):
        res = requests.get(f"{BACKEND_URL}/verify-image", params={"image_url": image_url})
        st.success(res.json())
