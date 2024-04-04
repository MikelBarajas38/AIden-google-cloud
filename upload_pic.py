import bucket

def upload_pic(bucket_name, file_path, blob_name='screenshot'):
    print(bucket.upload_to_bucket(bucket_name, blob_name, file_path, no_cache=True))
    print(f'Uploaded {file_path} to {bucket_name}')

if __name__ == "__main__":
    upload_pic('test-img-aiden', 'data/vid/test_0.avi', 'video')