import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# 1. Setup the Page Configuration
st.set_page_config(page_title="Vashishtha Family Invitation", page_icon="💌", layout="centered")

# 2. Add Custom CSS to make it beautiful (Maroon & Gold theme)
st.markdown("""
    <style>
    .stApp { background-color: #FEFBF6; }
    h1 { color: #800000; text-align: center; font-family: 'Georgia', serif; }
    p { text-align: center; font-size: 18px; color: #555; }
    .stButton>button { 
        background-color: #800000; 
        color: white; 
        border-radius: 8px; 
        padding: 10px 20px; 
        font-size: 18px; 
        width: 100%; 
        border: none;
    }
    .stButton>button:hover { background-color: #A52A2A; color: white; }
    #MainMenu {visibility: hidden;} /* Hides technical menu */
    footer {visibility: hidden;} /* Hides streamlit footer */
    </style>
""", unsafe_allow_html=True)

# 3. Create the simple, non-tech UI
st.markdown("<h1>💍 Vashishtha Family Wedding Invitation</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter a guest's name below to generate their personalized digital card.</p>", unsafe_allow_html=True)
st.write("---")

# The only thing your father sees: A text box
guest_name = st.text_input("✨ Enter the Guest's Name:", placeholder="e.g., Mr. Amit Sharma")

# If a name is typed, instantly prepare the PDF
if guest_name:
    try:
        # Create the transparent layer with the text
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", 16) 
        
        # NOTE: Adjust x (left/right) and y (up/down) to match the blank line on your card
        x_coordinate = 300
        y_coordinate = 200
        
        can.drawString(x_coordinate, y_coordinate, guest_name)
        can.save()
        packet.seek(0)
        new_pdf_with_name = PdfReader(packet)
        
        # Read the PDF directly from the folder (NO uploading required by the user!)
        with open("84665_2.pdf", "rb") as file:
            existing_pdf = PdfReader(file)
            output = PdfWriter()
            
            # Merge name onto the first page
            first_page = existing_pdf.pages[0]
            first_page.merge_page(new_pdf_with_name.pages[0])
            output.add_page(first_page)
            
            # Add remaining pages
            for i in range(1, len(existing_pdf.pages)):
                output.add_page(existing_pdf.pages[i])
                
            # Prepare for download
            output_stream = io.BytesIO()
            output.write(output_stream)
            output_stream.seek(0)
        
        # Show the download button with the custom file name
        st.success(f"🎉 Card ready for {guest_name}!")
        st.download_button(
            label=f"⬇️ Download PDF for {guest_name}",
            data=output_stream,
            file_name=f"Invitation_{guest_name}.pdf",
            mime="application/pdf"
        )
        
    except FileNotFoundError:
        st.error("System Error: The template file '84665_2.pdf' is missing from the server.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
