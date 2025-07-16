import streamlit as st

# Updated providers list with location and contact numbers
providers = [
    {'id': 1, 'name': 'Cherly', 'category': 'Cleaner', 'rating': 4.2, 
     'times': ['08:00 AM', '02:30 PM'], 'location': 'Nellmapis Ext-24', 'contact': '+27712345678'},
    {'id': 2, 'name': 'Matthew', 'category': 'Web Developer', 'rating': 5.0, 
     'times': ['09:00 AM', '03:30 PM'], 'location': 'Mamelodi Gardens', 'contact': '+27723456789'},
    {'id': 3, 'name': 'Mandla', 'category': 'Phomolong', 'rating': 3.9, 
     'times': ['06:00 AM', '06:00 PM'], 'location': 'Mamelodi West', 'contact': '+27734567890'},  
    {'id': 4, 'name': 'Given', 'category': 'Painter', 'rating': 5.0, 
     'times': ['07:00 AM', '12:30 PM'], 'location': 'Mahube', 'contact': '+27745678901'},  
    {'id': 5, 'name': 'Luyanda', 'category': 'Electrician', 'rating': 4.1, 
     'times': ['08:00 AM', '02:00 PM'], 'location': 'Lusaka', 'contact': '+27756789012'},  
    {'id': 6, 'name': 'Quinton', 'category': 'Gardener', 'rating': 5.0, 
     'times': ['09:00 AM', '03:30 PM'], 'location': 'Phase 5', 'contact': '+27767890123'},  
    {'id': 7, 'name': 'Antony', 'category': 'Transporter', 'rating': 2.3, 
     'times': ['09:00 AM', '09:30 PM'], 'location': 'Denneboom Hostel', 'contact': '+2778901234'},  
    {'id': 8, 'name': 'Siyabonga', 'category': 'FastFood', 'rating': 4.5, 
     'times': ['09:00 AM', '03:30 PM'], 'location': 'Skirlek', 'contact': '+27789012345'},  
    {'id': 9, 'name': 'Sophy', 'category': 'Laundry', 'rating': 5.0, 
     'times': ['09:00 AM', '03:30 PM'], 'location': 'Mamelodi 5&6', 'contact': '+27790123456'},  
    {'id': 10, 'name': 'Ayanda', 'category': 'Carpenter', 'rating': 5.0, 
     'times': ['09:00 AM', '03:30 PM'], 'location': 'Eestefabriek', 'contact': '+27701234567'}  
]

def main():
    st.title("FixIt Service Booking System")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.booking = {}
    
    # Step 0: Service category selection
    if st.session_state.step == 0:
        st.write("👋 Hello! Welcome to FixIt.")
        category = st.selectbox(
            "Select the service you need:",
            sorted(list(set([p['category'] for p in providers]))))
        
        if st.button("Next"):
            matched = [p for p in providers if p['category'].lower() == category.lower()]
            if not matched:
                st.error(f"Sorry, no providers available for '{category}'. Try something else")
            else:
                st.session_state.booking['category'] = category
                st.session_state.step = 1
                st.session_state.matched_providers = matched
                st.rerun()
    
    # Step 1: Provider selection (now with location and contact info)
    elif st.session_state.step == 1:
        st.write(f"Available {st.session_state.booking['category']}s:")
        
        # Create display strings with location and contact
        provider_options = {
            f"{p['id']}) {p['name']} - ⭐{p['rating']} | 📍{p['location']} | 📞{p['contact']}": p 
            for p in st.session_state.matched_providers
        }
        
        provider_choice = st.radio(
            "Select a provider:",
            options=list(provider_options.keys()))
        
        if st.button("Next"):
            selected_provider = provider_options[provider_choice]
            st.session_state.booking['provider'] = selected_provider
            st.session_state.step = 2
            st.rerun()
        
        if st.button("Back"):
            st.session_state.step = 0
            st.rerun()
    
    # Step 2: Time selection (unchanged)
    elif st.session_state.step == 2:
        provider = st.session_state.booking['provider']
        st.write(f"You chose {provider['name']}.")
        st.write(f"📍 Location: {provider['location']}")
        st.write(f"📞 Contact: {provider['contact']}")
        
        time_choice = st.radio(
            "Select a time:",
            options=provider['times'])
        
        if st.button("Next"):
            st.session_state.booking['time'] = time_choice
            st.session_state.step = 3
            st.rerun()
        
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()
    
    # Step 3: Payment confirmation (now shows contact info)
    elif st.session_state.step == 3:
        booking = st.session_state.booking
        provider = booking['provider']
        
        st.success(
            f"Booking summary:\n\n"
            f"Service: {booking['category']}\n"
            f"Provider: {provider['name']}\n"
            f"Location: {provider['location']}\n"
            f"Contact: {provider['contact']}\n"
            f"Time: {booking['time']}\n\n"
            "Please pay a deposit via Mpesa to 0766 355 966."
        )
        
        if st.checkbox("I have made the payment"):
            if st.button("Confirm Payment"):
                st.balloons()
                st.success(
                    f"✅ Payment confirmed!\n"
                    f"{provider['name']} will meet you at {booking['time']}.\n"
                    f"Contact them directly at {provider['contact']} if needed.\n\n"
                    "Thank you for using FixIt Booking."
                )
                del st.session_state.step
                del st.session_state.booking
                if st.button("Make another booking"):
                    st.rerun()
        
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()

if __name__ == '__main__':
    main() 