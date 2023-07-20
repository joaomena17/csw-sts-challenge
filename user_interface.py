import streamlit as st
import requests as r
from streamlit_option_menu import option_menu
from PIL import Image
         
def get_sensor_data_by_id(sensor_id):
    r.get(f"http://localhost:5000/sensors/{sensor_id}")

def main():
    #st.markdown("[!(csw.png)](www.criticalsoftware.com)")
    title, logo = st.columns([0.9,0.1])
    with title:
        st.title("Critical Summer Camp")
        st.markdown("""
                ## STS Challenge - **_IoT Project_**
                    """)
    with logo:
        image = Image.open("csw.png")
        st.write("\n\n")
        st.image(image, caption="Critical Software")
    st.divider()

    with st.sidebar:
        selected = option_menu("Smart Booking", ['Home', 'Search by ID', 'AI Chat', 'Book Now', ' Add Sensor'], 
            icons=['house', 'search', 'chat', 'cloud-upload', 'plus'], menu_icon="book", default_index=0)
        selected

    # HOME
    if selected == 'Home':

        st.write("### Smart Booking")
        st.write("Use this page to know everything that's happening in the office\n before you book a desk!")
        st.text("")

        st.write("##### What do you want to check out?")
        # insert buttons to select values
        col1, col2, col3, col4 = st.columns(4)
        user_params = [True, True, True, True]
        with col1:
            user_params[0] = st.checkbox("Temperature", value=True)

        with col2:
            user_params[1] = st.checkbox("CO2", value=True)

        with col3:
            user_params[2] = st.checkbox("Noise", value=True)

        with col4:
            user_params[3] = st.checkbox("Empty seats", value=True)


        st.markdown("***")
        st.write("##### Where do you want to check?")
        
        office_input  = "All"
        building_input  = "All"
        room_input = "All"

        office_input = st.selectbox("Select office:", ["All", "Porto", "Coimbra", "Lisboa"])
        building_input = "1"
        if office_input == "Coimbra":
            building_input = st.selectbox("Select building:", ["All","1","2","3"])
        if office_input != "All" and building_input != "All":
            room_input = st.selectbox("Select room:", ["All","1","2","3"])

        user_choice = [office_input, building_input, room_input]
        st.text("")
        st.button("Search now")
        st.markdown("***")

    # SEARCH BY ID
    if selected == 'Search by ID':
        st.write("### Search by ID")
        st.write("Use this page to fetch data from a sensor by entering it's unique ID")
        st.text("")
        sensor_id = st.text_input("Sensor ID", value="")
        id_search = st.button("Search now")
        if id_search:
            sensor_data = get_sensor_data_by_id(sensor_id)
        st.markdown("***")

    if selected == 'AI Chat':
        st.write("# WORK IN PROGRESS")
    

if __name__ == "__main__":
    main()
