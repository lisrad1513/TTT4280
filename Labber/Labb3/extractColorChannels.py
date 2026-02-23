import subprocess
import numpy as np
import os

def run_video_roi_extraction(video_path, output_path):
    """
    Call read_video_from_roi.py as a subprocess to extract ROI color channels from video.
    
    Args:
        video_path (str): Path to input video file
        output_path (str): Path to output data file
        
    Returns:
        bool: True if successful, False otherwise
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, '/Users/evenfinnoy/Documents/Skule/VSCODE/ELSYSS6/Sensor/Labber/Labb3/Optikk-lab-filer-26/read_video_from_roi.py')
    
    try:
        result = subprocess.run(
            ['python3', script_path, video_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running read_video_from_roi.py: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Script not found at {script_path}")
        return False



