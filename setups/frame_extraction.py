import cv2
import os

def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extracts frames from a video at a specified frame rate.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save extracted frames.
        frame_rate (int): Number of frames per second to extract.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        raise ValueError("FPS value is 0. Check the video file!")
    
    frame_interval = int(fps / frame_rate)
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save every nth frame based on the desired extraction rate
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Total frames extracted: {saved_count}")

# # Example usage:
video_file = 'C:\\Users\\manya\\Desktop\\yolo12\\media\\3cowvid.mp4'
frames_output_dir = 'C:\\Users\\manya\\Desktop\\yolo12\\output'
extract_frames(video_file, frames_output_dir, frame_rate=1)