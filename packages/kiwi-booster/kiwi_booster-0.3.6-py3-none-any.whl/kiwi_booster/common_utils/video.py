import cv2
import numpy as np


class VideoWriter:
    """Class for writing video frames to a local file"""

    def __init__(self, video_path: str, fps: int, codec: str = "MP4V") -> None:
        """Initializes the object.

        Args:
            video_path (str): Local path to the video file.
            fps (int): FPS of the video.
            codec (str, optional): Codec used to encode the video.
                Defaults to "MP4V".
        """
        self.video_path = video_path
        self.fps = fps
        self.codec = codec
        self.writer = None
        self.frame_id = 0

    def get_current_frame_id(self) -> int:
        """Returns the current frame id.

        Returns:
            int: Current frame id.
        """
        return self.frame_id

    def write_frame(self, frame: np.ndarray) -> None:
        """Writes frame to the video file.

        Args:
            frame (np.ndarray): Frame to write to the video file.
                It should be BGR.

        """
        if self.writer is None:
            self.writer = cv2.VideoWriter(
                self.video_path,
                cv2.VideoWriter_fourcc(*self.codec),
                int(self.fps),
                frame.shape[:2][::-1],
            )

        self.writer.write(frame)
        self.frame_id += 1

    def release(self) -> None:
        """Releases the video to close the file."""
        if self.writer is not None:
            self.writer.release()
