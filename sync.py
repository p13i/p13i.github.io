"""
Custom script to convert a Google Doc to a Markdown file for publishing to a
Jekyll post. I download and unzip an HTML file of my Google Doc and feed the 
path into the arguments of this script. The script converts the given HTML file
from Google Docs into a single-file HTML document with images embedded as 
base64 encoded images. The script also changes some of the HTML DOM to aid with
formatting of the post. Very custom!
"""

#region IMPORTS

import pickle
import re
from zipfile import ZipFile
import io
import os
import yaml
import sys
from typing import Dict, List
import html2text as html2text
from bs4 import BeautifulSoup, Tag
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

#endregion IMPORTS

#region CONSTANTS

GOOGLE_APIS_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
_DATA_GOOGLE_DOC_POSTS_YML = os.path.join('_data', 'google_doc_posts.yml')
CREDENTIALS_JSON = 'credentials.json'

#endregion CONSTANTS

#region MODELS


class MarkdownDocument:
    def __init__(self, front_matter: dict, lines: List[str], images: Dict[str, bytes], footnotes: Dict[str, str]):
        self.front_matter = front_matter
        self.lines = lines
        self.images = images
        self.footnotes = footnotes

    def __str__(self):
        # Set the markdown body
        markdown_contents = "\n".join(self.lines)

        # Join the footnotes into a string
        footnotes_str = '---\n' + '\n'.join(f'[^{id_}]: {text}' for id_, text in self.footnotes.items())

        # Prepend the jekyll front matter
        markdown_contents = f'---\n{yaml.dump(self.front_matter, width=sys.maxsize)}\n---\n{markdown_contents}\n{footnotes_str}'

        return markdown_contents

    def write(self, markdown_file_path, images_folder_path):
        # Write to the output markdown file
        with open(markdown_file_path, mode='wb+') as f:
            f.write(str(self).encode())

        # Write all the images
        for image_file_name, image_data in self.images.items():
            new_image_path = f'{images_folder_path}/{image_file_name}'

            # Create the directories if they don't exist
            if not os.path.exists(os.path.dirname(new_image_path)):
                os.makedirs(os.path.dirname(new_image_path), exist_ok=True)

            # Write to the file as binary
            with open(new_image_path, mode='wb') as f:
                f.write(image_data)

#endregion MODELS

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
                CREDENTIALS_JSON, GOOGLE_APIS_SCOPES)
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
    title = None
    author = None
    description = None
    jekyll_tags = []

    in_front_matter = False
    in_body = False
    reading_body = False

    def get_context(line_index, lines_up=3, lines_down=3):
        context_lines = []
        for i in range(line_index - lines_down, line_index + lines_up + 1):
            if 0 <= i < len(lines):
                s = lines[i]
                if i == line_index:
                    s += " <-- UNEXPECTED DIRECTIVE"
                context_lines.append(s)
        return '\n'.join(context_lines)

    for i, line in enumerate(lines):
        directive = line.strip()

        if i == 0 and directive.startswith('# '):
            title = directive[len('# '):]
            continue

        elif directive == '~':
            if in_front_matter:
                in_front_matter = False
                reading_body = in_body = True
                continue

            elif in_body:
                reading_body = in_body = read = False
                continue

            elif not in_front_matter and not in_body:
                in_front_matter = True
                continue

        elif directive.startswith('~'):
            if directive.startswith('~if'):
                option_name = directive[len('~if '):].strip()
                # Set the reading mode
                reading_body = options[option_name] if option_name in options else reading_body
                continue

            elif directive.startswith('~endif'):
                reading_body = in_body
                continue

        elif directive.startswith('#') and in_front_matter:
            tag = directive[1:]
            jekyll_tags.append(tag)
            continue

        elif directive.startswith('Author: '):
            if in_front_matter:
                author = directive[len('Author: '):]
                continue

        elif directive.startswith('Description: '):
            if in_front_matter:
                description = directive[len('Description: '):]
                continue

        elif reading_body:
            jekyll_lines.append(line)
            continue

        elif directive == '':
            continue

        elif directive == '* * *' and not in_body:
            break

        raise Exception(f'line {i}: unexpected directive: \n{get_context(i)}')

    if in_front_matter or in_body or reading_body:
        raise Exception('file does not contain an ending ~ or ~endif directive for jekyll. parsing failure. aborting.')

    return title, author, description, jekyll_lines, jekyll_tags


def html_to_markdown(html, output_images_server_path):
    FOOTNOTE_REGEX = re.compile(r'#ftnt([0-9]+)')

    # Pre-process the HTMl file

    soup = BeautifulSoup(html, features='html.parser')

    # Convert span blocks with "Courier New" in the style tag to code blocks
    for span in soup.find_all('span'):  # type: Tag
        if 'style' in span.attrs \
                and 'Courier New' in span.attrs['style'] \
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


def to_markdown(google_doc_id: str, output_images_site_path: str, options: {}) -> MarkdownDocument:
    front_matter = {}

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
    markdown_contents, footnotes = html_to_markdown(
        html=html_file_contents.decode('utf-8'),
        output_images_server_path=output_images_site_path,
    )

    # Only read the markdown we specified
    title, author, description, jekyll_lines, jekyll_tags = read_jekyll_content(
        markdown_contents=markdown_contents,
        options=options,
    )

    # Add to front matter
    front_matter['title'] = title
    front_matter['author'] = author
    front_matter['description'] = description
    front_matter['tags'] = jekyll_tags
    front_matter['layout'] = 'posts/post'

    return MarkdownDocument(
        front_matter=front_matter,
        lines=jekyll_lines,
        images=images,
        footnotes=footnotes,
    )

def main():
    if len(sys.argv) != 1:
        return print(help('sync'))

    with open(_DATA_GOOGLE_DOC_POSTS_YML, mode='r') as f:
        posts = yaml.load(f, Loader=yaml.FullLoader)

    for post in posts:
        # Read parameters
        google_doc_id = post['source']['id']
        output_markdown_file_path = post['output']['markdown']['file_path']
        output_markdown_options = post['output']['markdown']['options'] if 'options' in post['output'][
            'markdown'] else {}
        output_images_site_path = post['output']['images']['site_path']

        markdown: MarkdownDocument = to_markdown(google_doc_id, output_images_site_path, options=output_markdown_options)

        markdown.write(
            markdown_file_path=output_markdown_file_path,
            images_folder_path=output_images_site_path
        )


if __name__ == "__main__":
    main()
