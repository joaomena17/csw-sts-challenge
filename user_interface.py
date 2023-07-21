from webbrowser import get
import streamlit as st
import requests as r
from streamlit_option_menu import option_menu
from PIL import Image

def main():
    #st.markdown("[!(csw.png)](www.criticalsoftware.com)")
    title, team_logo, csw_logo = st.columns([0.9,0.1,0.1])
    with title:
        st.title("Critical Summer Camp")
        st.markdown("""
                ## STS Challenge - **_IoT Project_**
                    """)
        
    with team_logo:
        team_image = Image.open("logo.png")
        st.write("\n\n\n")
        st.image(team_image, caption="Clone Warriors")

    with csw_logo:
        image = Image.open("csw.png")
        st.write("\n\n")
        st.image(image, caption="Critical Software")
    st.divider()

    with st.sidebar:
        selected = option_menu("Smart Office", ['Home', 'Search by ID', 'AI Chat', ' Add Sensor'], 
            icons=['house', 'search', 'chat', 'plus'], menu_icon="book", default_index=0)
        selected
        print(selected)

    # HOME
    if selected == 'Home':

        st.write("### Smart Office")
        st.write("Use this page to know everything that's happening in the office\n before you book a desk!")
        #st.text("")

        #st.write("##### What do you want to check out?")
        # insert buttons to select values
        
        #col1, col2, col3, col4 = st.columns(4)
        #user_params = [True, True, True, True]
        #with col1:
        #    user_params[0] = st.checkbox("Temperature", value=True)

        #with col2:
        #    user_params[1] = st.checkbox("CO2", value=True)

        #with col3:
        #    user_params[2] = st.checkbox("Water", value=True)

        #with col4:
        #    user_params[3] = st.checkbox("Gas", value=True)


        #st.markdown("***")
        st.write("##### Where do you want to check?")
        
        office_input  = "All"
        building_input  = "All"
        room_input = "All"

        office_input = st.selectbox("Select office:", ["All", "Porto", "Coimbra", "Lisboa"])
        building_input = "Building 1"
        if office_input == "Coimbra":
            building_input = st.selectbox("Select building:", ["All","Building 1","Building 2","Building 3"])
        else: building_input = "All"

        if office_input == "Porto" or office_input == "Lisboa" or office_input == "Coimbra" and building_input != "All":
            room_input = st.selectbox("Select room:", ["All", "Building","Room 1","Room 2","Room 3"])
        
        if office_input == "Porto" or office_input == "Lisboa" and room_input != "All":
            building_input = "Building 1"


        st.text("")
        search_button = st.button("Search now")
        if search_button:
            if office_input == "All":
                response = r.get(f"http://localhost:5000/sensors")
                filter_data = response.json()
            elif office_input != "All" and building_input == "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}")
                filter_data = response.json()
            elif office_input != "All" and building_input != "All" and room_input == "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}/{building_input}")
                filter_data = response.json()
            elif office_input != "All" and building_input != "All" and room_input != "All":
                response = r.get(f"http://localhost:5000/sensors/{office_input}/{building_input}/{room_input}")
                print(f"http://localhost:5000/sensors/{office_input}/{building_input}/{room_input}")
                filter_data = response.json()
            if not filter_data:
                st.write("**No sensor found!**")
            else:
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
            if not sensor_data:
                st.write("**Sensor not found!**")
            else:
                st.dataframe(sensor_data)
        st.markdown("***")

    if selected == 'AI Chat':
        st.write("### Smart Assistant")
        st.write("Ask our intelligent smart assistant what you want to know and he will find that information for you.")
        user_query = st.text_area("Enter your request...")
        queries = [
            "Show all sensors",
            "Show the office, building and room with the highest temperature",
            "Show the office that has the room with the highest CO2 value",
            "Show all electricity values"
        ]
        predefined_query = st.selectbox("You can also use one of our pre-defined queries!", queries)

        if len(user_query) == 0:
            query_request = { "text": f"{predefined_query}"}
        else:
            query_request = { "text": f"{user_query}"}
        
        ai_button = st.button("Search now")
        if ai_button:
            response = r.post("http://localhost:5000/nlquery", json=query_request)
            if response.status_code == 200:
                st.dataframe(response.json())
            elif response.status_code != 200:
                st.write(response.json()["message"])
            else:
                st.write("Something went wrong...")

    # if selected == 'Book Room':message
    #    book_office = st.radio("Office", ["Porto", "Coimbra", "Lisboa"])
    #    if book_office == "Coimbra":message
    #    else:
    #        book_building = "A"
    #    book_room = st.radio("Room", ["Room1", "Room2", "Room3"])
    #    st.button("Check Availability")
    #    st.markdown("***")

        # Pie Chart
        # hyperlink to Pulsar
    
    if selected == ' Add Sensor':
        st.write("### Add Sensor")
        st.write("Fill the following fields to config<span style='color:green'>ure a new sensor to be monitored")
        st.text("")
        new_name = st.text_input("Sensor Name", value="")
        new_office = st.text_input("Office Location", value="")
        new_building = st.text_input("Building", value="")
        new_room = st.text_input("Room", value="")
        new_type = st.text_input("Sensor Type", value="")
        new_unit = st.text_input("Measuring Unit", value="")

        new_sensor = {
                        "name": f"{new_name}",
                        "office": f"{new_office}",
                        "building": f"{new_building}",
                        "room": f"{new_room}",
                        "type": f"{new_type}",
                        "units": f"{new_unit}"
                      }
        st.text("")

        add_sensor = st.button("Add Sensor")
        if add_sensor:
            print(new_sensor)
            response = r.post("http://localhost:5000/sensors", json=new_sensor)
        # TODO: green text success code 200 or sensor already exists
            if response.status_code == 200:
                st.write("<span style='color:green'>Sensor Registered Successfully!</span>",
                          unsafe_allow_html=True)
            elif response.status_code == 409:
                st.write("**Sensor already exists!**")
            elif response.status_code == 400:
                st.write(response.json()["message"])
            else:
                st.write("<span style='color:red'>Sensor registration failed!</span>",
                          unsafe_allow_html=True)
        st.markdown("***")


        # if add_sensor: POST
        # if response == 200: green text saying new sensor added successfuly
if __name__ == "__main__":
    main()
