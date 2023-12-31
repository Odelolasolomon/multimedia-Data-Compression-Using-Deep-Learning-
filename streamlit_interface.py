import streamlit as st
import os
import tfci
import subprocess

def compress_image(image_path, algorithm, quality):
    if algorithm == "Factorized Prior Autoencoder":
        subprocess.run(["python", "tfci.py", "compress", f"bmshj2018-factorized-msssim-{quality}", image_path])
        return image_path + ".tfci"
    elif algorithm == "Nonlinear transform coder model with factorized priors":
        subprocess.run(["python", "tfci.py", "compress", f"b2018-gdn-128-{quality}", image_path])
        return image_path + ".tfci"
    elif algorithm == "Hyperprior Model with Non Zero-Mean Gaussian Conditionals":
        subprocess.run(["python", "tfci.py", "compress", f"mbt2018-mean-msssim-{quality}", image_path])
        return image_path + ".tfci"
    # Add logic for the third algorithm

def decompress_image(image_path):
    decompressed_path = image_path.replace(".tfci.jpg", "_decompressed.jpg")
    subprocess.run(["python", "tfci.py", "decompress", image_path, decompressed_path])
    return decompressed_path

def main():
    st.title("Image Compression & Decompression App")

    operation = st.selectbox("Choose Operation", ["Compress", "Decompress"])
    if operation == 'Compress':
        uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg', 'tfci'])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
            algorithm = st.selectbox("Choose Compression Algorithm", [
                "Factorized Prior Autoencoder", 
                "Nonlinear Transform Coder Model with Factorized Priors", 
                "Hyperprior Model with Non Zero-Mean Gaussian Conditionals"
            ])

            if algorithm == "Factorized Prior Autoencoder":
                quality = st.selectbox("Select a quality level", [1, 2, 3, 4, 5, 6, 7, 8])
            elif algorithm == "Nonlinear Transform Coder Model with Factorized Priors":
                quality = st.selectbox("Select a quality level", [1, 2, 3, 4])
            elif algorithm == "Hyperprior Model with Non Zero-Mean Gaussian Conditionals":
                quality = st.selectbox("Select a quality level", [1, 2, 3, 4, 5, 6, 7, 8])
            
        #temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")  # you can adjust the suffix based on the uploaded file type
        #temp_file.write(uploaded_image.read())
        
            if st.button("Execute"):
                    # Call the function to compress
                compressed_file = compress_image(uploaded_image.name, algorithm, quality)
                st.write("Compression Done!")
                    #st.download_button('Download Compressed File', data=compressed_file)
                with open(compressed_file, 'rb') as f:
                    st.download_button('Download Compressed File', f, file_name=compressed_file)
                      #  st.download_button(label="", data=compressed_file)

    elif operation == 'Decompress':
        uploaded_decompressed = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg', 'tfci'])
        if uploaded_decompressed:
            if st.button('Execute'):
                decompressed_file = decompress_image(uploaded_decompressed.name)
                st.image(decompressed_file, caption="Decompressed Image", use_column_width=True)
                st.write("Decompression Done!")
                with open(decompressed_file, 'rb') as f:
                    st.download_button('Download Compressed File', f, file_name=decompressed_file)

if __name__ == "__main__":
    main()
