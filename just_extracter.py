import zipfile
import os

def extract_zip_file(zip_file_name, destination):
    zip_ref = zipfile.ZipFile(zip_file_name, 'r')
    zip_ref.extractall(destination)
    zip_ref.close()

if __name__ == "__main__":

    data_dir = '../wider/images'

    train_images = 'WIDER_train.zip'
    val_images = 'WIDER_val.zip'
    test_images = 'WIDER_test.zip'

    to_extract = [train_images, val_images, test_images]
    destinations = [data_dir + '/' + ims for ims in to_extract]

    for imgs in to_extract:
        print(f'extracting {imgs}')
        extract_zip_file(os.path.join(data_dir, imgs), data_dir)

    annotation_zip_file = "wider_face_split.zip"
    print("extracting annotations")
    extract_zip_file(os.path.join(data_dir, annotation_zip_file), data_dir)

    print('done!')

