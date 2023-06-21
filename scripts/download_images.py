import os
import requests
import sys

def download_images(url_list_file, local_folder):
    # Create the local folder if it doesn't exist
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # Read the list of image URLs from the file
    with open(url_list_file, "r") as f:
        image_urls = f.read().splitlines()

    # Download and save each image
    for image_url in image_urls:
        # Extract the image file name from the URL
        image_filename = os.path.basename(image_url)

        # Download the image
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(os.path.join(local_folder, image_filename), "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {image_filename}")
            else:
                print(f"Failed to download: {image_filename}")
        except Exception as e:
            print(f"Failed to download: {image_filename}. Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python download_images.py /path/to/url_list.txt /path/to/local/folder")
        exit(1)
    # Get the path to the file containing the list of image URLs and local folder from command-line arguments
    url_list_file = sys.argv[1]
    local_folder = sys.argv[2]

    download_images(url_list_file, local_folder)
