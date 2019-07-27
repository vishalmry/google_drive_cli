import auth
import json
import io
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
            if (individual_files['name'] == file_name) :
                return individual_files['id']

        if page_token is None:
            return None

def download_file(file_name) :
    get_ID = search_file(file_name)
    get_ID = str(get_ID)
    if get_ID is None :
        print ("The file does not exists")
        return
    print (get_ID)
    response_recieved = drive_service.files().get_media(fileId = get_ID)
    print ('till here')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, response_recieved)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

download_file('IDM 6.27 Build 2 Registered (32bit + 64bit Patch) [CrackingPatching].rar')


