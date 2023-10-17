import streamlit as st 
from PIL import Image
import io
import pdfplumber
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

def extract_text_from_pdf(pdf_file):
    if pdf_file is not None:
        pdf_data = pdf_file.read()  
    
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            pdf_text = ""
            for pg in pdf.pages:
             pdf_text += pg.extract_text()
            #. pdf_extract()
            
    return pdf_text

# Function to perform text summarization using spaCy
def spacy_summarize(text, max_words=500):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Create a list of sentences with their respective weights based on word frequency
    sentence_weights = {}
    for sentence in doc.sents:
        sentence_text = sentence.text.lower()
        for word in sentence_text.split():
            if word not in STOP_WORDS:
                if sentence not in sentence_weights:
                    sentence_weights[sentence] = 1
                else:
                    sentence_weights[sentence] += 1

    # Sort sentences by weight in descending order
    sorted_sentences = sorted(sentence_weights, key=lambda x: sentence_weights[x], reverse=True)

    # Generate the summary
    summary = ""
    word_count = 0
    for sentence in sorted_sentences:
        if word_count + len(sentence.text.split()) <= max_words:
            summary += sentence.text
            word_count += len(sentence.text.split())
        else:
            break

    return summary

# Streamlit app
def main():
    # Use HTML tags to style the title with color
    title_html = """
    <h1 style="color: purple;"><u>PDF Summarizer with spaCy</u></h1>
    """
    st.markdown(title_html, unsafe_allow_html=True)
    
    st.sidebar.write("## Upload  An Input file :")       
    # Add a file uploader widget
    pdf_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
    
    # Add an image to the title section
    image_path = 'C:/Users/Ftk/Desktop/streamlit/nlp/text_sum_symbol.png'
    image = Image.open(image_path)

    # Display the image using st.image()
    st.sidebar.image(image, caption="Text Summerization", use_column_width=True)

    # Check if a PDF file is uploaded
    if pdf_file is not None:
        st.sidebar.write("PDF File Uploaded:", pdf_file.name)
        
        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(pdf_file)

        # Summarize the PDF content to 500 words using spaCy
        summarized_text = spacy_summarize(pdf_text, max_words=500)
        header_html ="""
        <h3 style="color: blue">Summary (500 words)</h3>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Define custom CSS styles to change the font color
        custom_css = """
        <style>
        .summary-text {
            color:  blue;font-family: 'Arial', sans-serif; /* Change the font family to your desired font */
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)

        # Use the custom CSS style to format the summary text
        st.markdown(f'<p class="summary-text">{summarized_text}</p>', unsafe_allow_html=True)
          
if __name__ == "__main__":
    main()
