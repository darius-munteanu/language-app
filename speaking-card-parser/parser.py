import os
import fitz  # PyMuPDF

def pdf_to_pngs(pdf_path):
    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"File {pdf_path} does not exist.")
        return

    # Create 'output' directory if it does not exist
    output_dir = "C:/language-app/speaking-card-parser/output"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Open the PDF file
    pdf = fitz.open(pdf_path)

    # Convert each page to a PNG
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        pix = page.get_pixmap()

        output_file = f"{output_dir}/page_{page_num + 1}.png"
        pix.save(output_file)
        print(f"Saved {output_file}")

    # Close the PDF file
    pdf.close()
    print("Conversion completed.")

if __name__ == "__main__":
    pdf_to_pngs("C:/language-app/speaking-card-parser/asqp.pdf")