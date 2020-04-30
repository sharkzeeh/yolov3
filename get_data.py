import requests
import os
from just_extracter import extract_zip_file

data_dir = '../wider/images'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def download_file_from_web_server(url, destination):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    response = requests.get(url, stream=True)
    save_response_content(response, os.path.join(destination, local_filename))

    return local_filename


#  TODO Add progress bar
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":


    train_images = 'WIDER_train.zip'
    val_images = 'WIDER_val.zip'
    test_images = 'WIDER_test.zip'
    annotation_url = 'http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/support/bbx_annotation/wider_face_split.zip'

    file_ids = ['17i_8a1nwFFGdplDNThisWbbpqvMQiyJf',
				'1-q3w1amXlyNNHz4x7U1NQn36rGzAnEIf',
				'1gnvl7iv4ExHuAUkdeQkX-W1UlW90mVJ9']

    to_download = [train_images, val_images, test_images]    

    destinations = [data_dir + '/' + ims for ims in to_download]

    for file_id, destination in zip(file_ids, destinations):
        print(f"downloading {destination.split('/')[1]} from google drive...")
        download_file_from_google_drive(file_id, destination)

    for imgs in to_download:
        print(f'extracting {imgs}')
        extract_zip_file(os.path.join(data_dir, imgs), data_dir)

    print('downloading the bounding boxes annotations...')
    annotation_zip_file = download_file_from_web_server(annotation_url,
                                                        data_dir)

    extract_zip_file(os.path.join(data_dir, annotation_zip_file), data_dir)

    print('done')
