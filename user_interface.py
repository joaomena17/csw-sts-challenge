import streamlit as st
import requests as r
from streamlit_option_menu import option_menu
from PIL import Image

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
        selected = option_menu("Smart Booking", ['Home', 'Search by ID', 'AI Chat', 'Book Room', ' Add Sensor'], 
            icons=['house', 'search', 'chat', 'cloud-upload', 'plus'], menu_icon="book", default_index=0)
        selected
        print(selected)

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

        st.text("")
        search_button = st.button("Search now")
        if search_button:
            if office_input == "All":
                response = r.get(f"http://localhost:5000/sensors/")
                filter_data = response.json()
            elif office_input != "All" and building_input == "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}")
                filter_data = response.json()
            elif office_input != "All" and building_input != "All" and room_input == "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}/{building_input}")
                filter_data = response.json()
            elif office_input != "All" and building_input != "All" and room_input != "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}/{building_input}/{room_input}")
                filter_data = response.json()
            st.dataframe(filter_data)
        st.markdown("***")

    # SEARCH BY ID
    if selected == 'Search by ID':
        st.write("### Search by ID")
        st.write("Use this page to fetch data from a sensor by entering it's unique ID")
        st.text("")
        sensor_id = st.text_input("Sensor ID", value="")
        id_search = st.button("Search now")
        if id_search:
            response = r.get(f"http://localhost:5000/sensors/{sensor_id}")
            sensor_data = response.json()
            st.dataframe(sensor_data)
        st.markdown("***")

    if selected == 'AI Chat':
        st.write("# WORK IN PROGRESS")

    if selected == 'Book Room':
        st.write("### Book Room")
        st.write("Select the room you want to book and check if it's available.")
        st.text("")
        book_office = st.radio("Office", ["Porto", "Coimbra", "Lisboa"])
        if book_office == "Coimbra":
            book_building = st.radio("Building", ["A", "B", "C"])
        else:
            book_building = "A"
        book_room = st.radio("Room", ["Room1", "Room2", "Room3"])
        st.button("Check Availability")
        st.markdown("***")

        # Pie Chart
        # hyperlink to Pulsar
    
    if selected == ' Add Sensor':
        st.write("### Add Sensor")
        st.write("Fill the following fields to add a new sensor to the MQTT Broker.")
        st.text("")
        new_name = st.text_input("Sensor Name", value="")
        new_office = st.text_input("Office Location", value="")
        new_building = st.text_input("Building", value="")
        new_room = st.text_input("Room", value="")
        new_type = st.text_input("Sensor Type", value="")
        new_unit = st.text_input("Measuring Unit", value="")
        st.text("")

        add_sensor = st.button("Add Sensor")
        st.markdown("***")


        # if add_sensor: POST
        # if response == 200: green text saying new sensor added successfuly
if __name__ == "__main__":
    main()
