import kagglehub

# Download latest version
path = kagglehub.dataset_download("fandaoerji/cbvd-5cow-behavior-video-dataset")

print("Path to dataset files:", path)