import subprocess
import numpy as np
import os


def _trim_output_file(output_path, fps, remove_first_n_seconds=0, remove_last_n_seconds=0):
    data = np.loadtxt(output_path)
    if data.ndim == 1:
        data = data[np.newaxis, :]

    first_frames = int(max(0, remove_first_n_seconds) * fps)
    last_frames = int(max(0, remove_last_n_seconds) * fps)

    start_idx = first_frames
    end_idx = data.shape[0] - last_frames if last_frames > 0 else data.shape[0]
    end_idx = max(start_idx, end_idx)

    trimmed = data[start_idx:end_idx, :]
    np.savetxt(output_path, trimmed)

    if first_frames > 0:
        print(f"Removed first {remove_first_n_seconds} seconds ({first_frames} frames)")
    if last_frames > 0:
        print(f"Removed last {remove_last_n_seconds} seconds ({last_frames} frames)")

def run_video_roi_extraction(video_path, output_path, remove_first_n_seconds=0, remove_last_n_seconds=0, fps=30.0):
    """
    Call read_video_from_roi.py as a subprocess to extract ROI color channels from video.
    
    Args:
        video_path (str): Path to input video file
        output_path (str): Path to output data file
        remove_first_n_seconds (int): Number of seconds to remove from the beginning of the output file
        remove_last_n_seconds (int): Number of seconds to remove from the end of the output file
        fps (float): Video frame rate used for time-to-frame trimming conversion
        
    Returns:
        bool: True if successful, False otherwise
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'Optikk-lab-filer-26', 'read_video_from_roi.py')
    
    try:
        result = subprocess.run(
            ['python3', script_path, video_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)

        if remove_first_n_seconds > 0 or remove_last_n_seconds > 0:
            _trim_output_file(output_path, fps, remove_first_n_seconds, remove_last_n_seconds)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running read_video_from_roi.py: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Script not found at {script_path}")
        return False



