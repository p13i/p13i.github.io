"""
Custom script to convert a Google Doc to a Markdown file for publishing to a
Jekyll post. I download and unzip an HTML file of my Google Doc and feed the 
path into the arguments of this script. The script converts the given HTML file
from Google Docs into a single-file HTML document with images embedded as 
base64 encoded images. The script also changes some of the HTML DOM to aid with
formatting of the post. Very custom!
"""
import io

import html2text as html2text
from bs4 import BeautifulSoup, Tag
from zipfile import ZipFile
import sys
import base64
import os
import re
import yaml
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaIoBaseDownload

GOOGLE_APIS_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

_DATA_GOOGLE_DOC_POSTS_YML = os.path.join('_data', 'google_doc_posts.yml')


def get_drive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', GOOGLE_APIS_SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service


def get_google_doc_html_zipped(google_doc_id) -> io.BytesIO:
    drive = get_drive_service()

    request = drive.files().export_media(fileId=google_doc_id, mimeType='application/zip')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return fh


def read_jekyll_content(markdown_contents, options):
    lines = markdown_contents.splitlines()

    jekyll_lines = []

    in_front_matter = False
    in_body = False
    reading_body = False

    for line in lines:
        directive = line.strip()

        if directive == '~':
            if in_front_matter:
                in_front_matter = False
                reading_body = in_body = True
            elif in_body:
                reading_body = in_body = False
            elif not in_front_matter and not in_body:
                in_front_matter = True

        elif directive.startswith('~'):
            if directive.startswith('~if'):
                option_name = directive[len('~if '):].strip()
                # Set the reading mode
                reading_body = options[option_name] if option_name in options else reading_body
            elif directive.startswith('~endif'):
                reading_body = in_body

        elif reading_body:
            jekyll_lines.append(line)

    if in_front_matter or in_body or reading_body:
        raise Exception('file does not contain an ending ~ or ~endif directive for jekyll. parsing failure. aborting.')

    return '\n'.join(jekyll_lines)


def html_to_markdown(html, output_images_server_path):
    FOOTNOTE_REGEX = re.compile(r'#ftnt([0-9]+)')

    # Pre-process the HTMl file

    soup = BeautifulSoup(html)

    # Convert span blocks with "Courier New" in the style tag to code blocks
    for span in soup.find_all('span'):  # type: Tag
        if 'style' in span.attrs \
                and 'Courier New' in span.attrs['style']\
                and len(span.get_text().strip()) > 0:

            a = span.find('a')
            if a:
                href = a.attrs['href']
                new_tag = BeautifulSoup(f'<a href="{href}"><code>{span.get_text()}</code></a>', features='html.parser')
            else:
                new_tag = BeautifulSoup(f'<code>{span.get_text()}</code>', features='html.parser')

            span.replace_with(new_tag)

    # Make every a tag a target blank
    for a in soup.find_all('a'):
        a.attrs['target'] = '_blank'

    # Link the images
    for img in soup.find_all('img'):
        src = img.attrs['src']
        src = src[len('images/'):]
        img.attrs['src'] = f'{output_images_server_path}/{src}'

        # Make it full-width
        img.attrs['width'] = '100%'

    # Extract footnotes
    footnotes = {}
    for a in soup.find_all('a'):  # type: Tag
        if 'href' in a.attrs and FOOTNOTE_REGEX.search(a.attrs['href']):

            # Get the footnote id from the href (removing the starting # character)
            footnote_id = a.attrs['href'][1:]

            footnote_a = soup.find(attrs={'id': footnote_id})
            footnote_text = footnote_a.next_sibling.get_text()

            footnotes[footnote_id] = footnote_text

            # Remove the footnote elements from the HTML
            a.replace_with(BeautifulSoup(f'[^{footnote_id}]', features='html.parser'))
            footnote_a.extract()

    # Convert!
    markdown = html2text.html2text(str(soup), bodywidth=0)
    return markdown, footnotes


def pull_from_google_docs():
    with open(_DATA_GOOGLE_DOC_POSTS_YML, mode='r') as f:
        posts = yaml.load(f)

    for post in posts:
        # Read parameters
        google_doc_id = post['source']['id']
        output_markdown_file_path = post['output']['markdown']['file_path']
        output_markdown_options = post['output']['markdown']['options']
        output_images_server_path = post['output']['images']['server_path']
        front_matter = post['front_matter']

        # Read the zip file from Google Drive
        zip_fh = get_google_doc_html_zipped(google_doc_id)
        zip_file = ZipFile(zip_fh)

        # Read the HTML file into memory
        html_file_name = next(name for name in zip_file.namelist() if name.endswith('.html'))
        with zip_file.open(html_file_name, mode='r') as html_file:
            html_file_contents = html_file.read()

        # Read each image into memory
        image_file_names = [name for name in zip_file.namelist() if name.startswith('images')]
        images = {}
        for image_file_name in image_file_names:
            with zip_file.open(image_file_name, mode='r') as image_file:
                image_file_name = image_file_name[len('images/'):]
                images[image_file_name] = image_file.read()

        # Convert the HTML to Markdown
        markdown_contents, footnotes = html_to_markdown(html_file_contents.decode('utf-8'), output_images_server_path)

        # Only read the markdown we specified
        markdown_contents = read_jekyll_content(markdown_contents, options=output_markdown_options)

        # Join the footnotes into a string
        footnotes_str = '---\n' + '\n'.join(f'[^{id_}]: {text}' for id_, text in footnotes.items())

        # Prepend the jekyll front matter
        markdown_contents = f'---\n{yaml.dump(front_matter)}\n---\n{markdown_contents}\n{footnotes_str}'

        # Write to the output markdown file
        with open(output_markdown_file_path, mode='wb+') as f:
            f.write(markdown_contents.encode())

        for image_file_name, image_data in images.items():
            new_image_path = f'{output_images_server_path}/{image_file_name}'

            if not os.path.exists(os.path.dirname(new_image_path)):
                os.makedirs(os.path.dirname(new_image_path), exist_ok=True)

            with open(new_image_path, mode='wb') as f:
                f.write(image_data)

def main():
    pull_from_google_docs()


def main2():
    if len(sys.argv) != 3:
        print(help())
        return

    _, html_path, markdown_path = sys.argv

    enclosing_folder = os.path.dirname(html_path)

    with open(html_path, mode='r') as html_file:
        html = html_file.read()

    soup = BeautifulSoup(html, features='html.parser')

    for img in soup.findAll('img'):
        local_img_path = os.path.join(enclosing_folder, img['src'])

        _, img_extension = os.path.splitext(local_img_path)
        img_extension = img_extension[1:]  # remove dot (".")

        with open(local_img_path, mode='rb') as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        img_data = f'data:image/{img_extension};base64,{encoded_string}'

        img['src'] = img_data

    # Remove classes from the <body> tag as it interferes with existing styling
    soup.body['class'] = ''

    # Add float-right class to tags in Table of Contents
    for a in soup.findAll('a'):
        if 'href' in a.attrs \
                and re.search(r'#h\.[a-z0-9]+', a['href']) \
                and re.search(r'[0-9]+', a.text):
            parent = a.find_parent()
            if 'class' in parent.attrs:
                parent.attrs['class'].append('float-right')

    # Include content after this indicator
    jekyll_start = list(soup(text='!jekyll::start'))

    if not jekyll_start:
        print('html file must have text literal !jekyll::start')
        return

    start_tag = jekyll_start[0]
    while start_tag.name != 'p':
        start_tag = start_tag.parent

    body_after_start = start_tag.find_next_siblings()
    body_after_start_html_str = ''.join(tag.prettify() for tag in body_after_start if tag)

    inline_img_html_string = soup.head.prettify() + '\n' + body_after_start_html_str

    markdown_front_matter = get_front_matter(markdown_path)

    if not markdown_front_matter:
        print('no matches in markdown front matter')
        return

    with open(markdown_path, mode='w+') as markdown_file:
        markdown_file.write(markdown_front_matter + '\n' + inline_img_html_string)


def get_front_matter(markdown_path):
    in_front_matter = False
    front_matter_lines = []
    with open(markdown_path, mode='r') as markdown_file:
        for line in markdown_file:
            triple_dash_found = line.find('---') > -1

            if not in_front_matter and triple_dash_found:
                in_front_matter = True

            elif in_front_matter and triple_dash_found:
                break

            elif in_front_matter:
                front_matter_lines.append(line)

    return '---\n' + ''.join(front_matter_lines) + '---\n'


def help():
    return """
    python3 gdoc2markdown.py <input html file> <output markdown file>
        input html file: path to the HTML file in the unzipped Google Doc
        output markdown file: path to write markdown contents to
    """


if __name__ == "__main__":
    main()
