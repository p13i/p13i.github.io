import os
import re
import sys

def get_all_image_urls(source_code_folder, output_file):
    # Find all image URLs in the source code files using a regular expression
    image_urls = []
    extensions = [".html", ".md", ".yaml", ".yml"]
    for root, dirs, files in os.walk(source_code_folder):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    source_code = f.read()
                    image_urls.extend(re.findall(r'https?://[^\s/$.?#\":].[^\s\",:]*\.(?:png|jpe?g|gif)', source_code))
    
    # Depulicate and sort URLs
    image_urls = sorted(list(set(image_urls)))

    # Write the list of image URLs to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(image_urls))

    print(f"List of {len(image_urls)} image URLs written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python get_all_image_urls.py /path/to/source/code /path/to/output_file.txt")
        exit(1)

    # Get the source code folder and output file path from command-line arguments
    source_code_folder = sys.argv[1]
    output_file = sys.argv[2]

    get_all_image_urls(source_code_folder, output_file)
