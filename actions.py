#!/usr/bin/env python3
import auth
import json
import io
from apiclient import http
from apiclient import errors
from apiclient.http import MediaIoBaseDownload

"The first thing to do now is to send and get an http response"
drive_service = auth.main()

def list_files() :
    all_files = []
    page_token = None
    while True:
        files = drive_service.files().list(
            pageToken = page_token
        ).execute()

        page_token = files.get('nextPageToken', None)

        files = files["files"]
        for individual_files in files:
            individual_files = individual_files['name']
            all_files.append(individual_files)

        if page_token is None:
            break

    return all_files

def search_file(file_name) :
    page_token = None
    while True:
        files = drive_service.files().list(
            pageToken = page_token
        ).execute()

        page_token = files.get('nextPageToken', None)

        files = files["files"]
        for individual_files in files:
            if (file_name in individual_files['name']) :
                return individual_files['id']

        if page_token is None:
            return None

def download_file(file_name) :
    get_ID = search_file(file_name)
    get_ID = str(get_ID)
    if get_ID is None :
        print ("The file does not exists")
        return

    response_recieved = drive_service.files().get_media(fileId = get_ID)
    fh = io.BytesIO()
    downloader = http.MediaIoBaseDownload(fh, response_recieved)

    # Download the file
    done = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
        except errors.HttpError:
            print ('An error occurred')
        if status:
            print ('Download Progress: %d%%' % int(status.progress() * 100))
        if done:
            print ("Download %d%%." % int(status.progress() * 100))
        with open(file_name, 'wb') as downloaded_file:
            downloaded_file.write(fh.getvalue())

download_file('IDM 6.27 Build 2 Registered (32bit + 64bit Patch) [CrackingPatching].rar')


