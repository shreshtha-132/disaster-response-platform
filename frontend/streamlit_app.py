import streamlit as st
import requests
import uuid

def is_valid_uuid(u):
    try:
        uuid.UUID(u)
        return True
    except:
        return False

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
    tags = st.text_input("Tags (comma-separated)")
    owner_id = st.text_input("Owner ID")

    if st.button("Submit Report"):
        if not title or not description:
            st.warning("Title and Description are required.")
        else:
            tags = [t.strip() for t in tags.split(",") if t.strip()]
            data = {
                "title": title,
                "description": description,
                "tags": tags,
                "owner_id": owner_id
            }
            with st.spinner("Reporting disaster..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/disasters", json=data)
                    res.raise_for_status()
                    st.success("✅ Disaster reported successfully!")
                    st.json(res.json())
                except Exception as e:
                    st.error(f"❌ Failed to report disaster: {e}")

elif section == "Get All Disasters":
    st.subheader("📄 List of All Disasters")
    try:
        res = requests.get(f"{BACKEND_URL}/disasters")
        res.raise_for_status()
        disasters = res.json()["disasters"]

        if not disasters:
            st.info("No disasters reported yet.")
        else:
            for d in disasters:
                with st.expander(f"{d['title']} — {d.get('location_name', 'Unknown')}"):
                    st.markdown(f"**🆔 ID:** `{d['id']}`")
                    st.markdown(f"**📍 Location:** {d.get('location_name', 'Unknown')}")
                    st.markdown(f"**📝 Description:** {d['description']}")
                    st.markdown(f"**🏷 Tags:** `{', '.join(d['tags'])}`")
                    st.markdown(f"**👤 Owner ID:** `{d['owner_id']}`")
                    st.markdown(f"**📅 Created:** `{d['created_at']}`")
    except Exception as e:
        st.error(f"Error fetching disasters: {str(e)}")



elif section == "Update Disaster":
    st.subheader("🛠 Update Existing Disaster")
    new_title = st.text_input("✏️ New Title (optional)")
    disaster_id = st.text_input("🆔 Disaster ID (UUID)")
    new_desc = st.text_area("New Description")
    owner_id = st.text_input("Updater Owner ID")
    new_tags_input = st.text_input("🏷 New Tags (comma-separated, optional)")

    if st.button("🔄 Update Disaster"):
        if not disaster_id:
            st.warning("Please enter a valid Disaster ID.")
        else:
            update_data = {}
            if new_title:
                update_data["title"] = new_title
            if new_desc:
                update_data["description"] = new_desc
            if new_tags_input:
                tags = [t.strip() for t in new_tags_input.split(",") if t.strip()]
                update_data["tags"] = tags
            if owner_id:
                update_data["owner_id"] = owner_id

            if not update_data:
                st.info("No fields to update.")
            else:
                with st.spinner("Updating disaster..."):
                    try:
                        res = requests.put(f"{BACKEND_URL}/disasters/{disaster_id}", json=update_data)
                        res.raise_for_status()
                        st.success("✅ Disaster updated successfully!")
                        st.json(res.json())
                    except Exception as e:
                        st.error(f"❌ Failed to update disaster: {e}")

elif section == "Delete Disaster":
    st.subheader("❌ Delete Disaster by ID")
    disaster_id = st.text_input("Disaster ID (UUID)")
    if st.button("Delete Disaster"):
        if not disaster_id:
            st.warning("Please provide a valid Disaster ID.")
        else:
            try:
                res = requests.delete(f"{BACKEND_URL}/disasters/{disaster_id}")
                if res.ok:
                    st.success(res.json().get("message", "Disaster deleted."))
                    st.json(res.json())
                else:
                    st.error(res.json().get("detail", "Something went wrong."))
            except Exception as e:
                st.error(f"Error: {e}")

elif section == "Add Resource":
    st.subheader("➕ Add Resource to Disaster")

    disaster_id = st.text_input("Disaster ID")
    name = st.text_input("Resource Name")
    location_name = st.text_input("Location Name")
    type_ = st.text_input("Resource Type")

    if st.button("Add Resource"):
        if not (disaster_id and name and location_name and type_):
            st.warning("Please fill all fields.")
        elif not is_valid_uuid(disaster_id):
            st.error("❌ Invalid Disaster ID. Please enter a valid UUID.")
        else:
            data = {
                "disaster_id": disaster_id,
                "name": name,
                "location_name": location_name,
                "type": type_
            }
            try:
                res = requests.post(f"{BACKEND_URL}/resources", json=data)
                if res.ok:
                    st.success(res.json().get("message", "Resource added."))
                    st.json(res.json())
                else:
                    st.error(res.json().get("detail", "Failed to add resource."))
            except Exception as e:
                st.error(f"Error: {e}")


elif section == "Resources by Disaster ID":
    st.subheader("🔎 Resources Linked to a Disaster")
    disaster_id = st.text_input("Disaster ID (UUID)")
    if st.button("Fetch Resources"):
        if not disaster_id:
            st.warning("⚠️ Please enter a Disaster ID.")
        elif not is_valid_uuid(disaster_id):
            st.error("❌ Invalid UUID format for Disaster ID.")
        else:
            try:
                res = requests.get(f"{BACKEND_URL}/resources/{disaster_id}/resources")
                if res.ok:
                    resources = res.json().get("Resources", [])
                    if not resources:
                        st.info("ℹ️ No resources found for this disaster.")
                    else:
                        st.success(f"✅ Found {len(resources)} resources.")
                        for r in resources:
                            with st.expander(r["name"]):
                                st.json(r)
                else:
                    st.error(res.json().get("detail", "Failed to fetch resources."))
            except Exception as e:
                st.error(f"Error: {e}")


elif section == "Resources by Location":
    st.subheader("🌍 Find Resources Nearby")
    location_name = st.text_input("Enter Location Name")
    if st.button("Find Resources"):
        if not location_name.strip():
            st.warning("⚠️ Please enter a valid location name.")
        else:
            try:
                res = requests.get(f"{BACKEND_URL}/resources/by-location/{location_name}")
                if res.status_code == 200:
                    data = res.json()
                    resources = data.get("Resources", [])
                    if resources:
                        st.success(f"✅ Found {len(resources)} resources near '{location_name}'")
                        for r in resources:
                            with st.expander(f"📌 {r['name']} ({r['type']})"):
                                st.json(r)
                    else:
                        st.info(f"No resources found near '{location_name}'")
                else:
                    error_msg = res.json().get("detail", "Something went wrong")
                    st.error(f"❌ {error_msg}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")


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
