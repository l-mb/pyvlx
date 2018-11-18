"""Module for retrieving scene list from API."""
from pyvlx.frame_activate_scene import FrameActivateSceneRequest, FrameActivateSceneConfirmation, ActivateSceneConfirmationStatus
from pyvlx.frame_command_send import FrameSessionFinishedNotification, FrameCommandRunStatusNotification
from pyvlx.api_event import ApiEvent
from pyvlx.session_id import get_new_session_id


class ActivateScene(ApiEvent):
    """Class for retrieving scene list from API."""

    def __init__(self, connection, scene_id, wait_for_completion=True, timeout_in_seconds=60):
        """Initialize SceneList class."""
        super().__init__(connection, timeout_in_seconds)
        self.success = False
        self.scene_id = scene_id
        self.wait_for_completion = wait_for_completion
        self.session_id = None

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameActivateSceneConfirmation) and frame.session_id == self.session_id:
            if frame.status == ActivateSceneConfirmationStatus.ACCEPTED:
                self.success = True
            return not self.wait_for_completion
        if isinstance(frame, FrameCommandRunStatusNotification) and frame.session_id == self.session_id:
            # At the moment I don't reall understand what the FrameCommandRunStatusNotification is good for.
            # Ignoring these packets for now
            return False
        if isinstance(frame, FrameSessionFinishedNotification) and frame.session_id == self.session_id:
            return True

        print("Not handling: ", frame)
        return False

    def request_frame(self):
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameActivateSceneRequest(scene_id=self.scene_id, session_id=self.session_id)