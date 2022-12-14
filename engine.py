# Method to pass keyboard inputs to the game (sentdex)
# Method to pass mouse inputs to the game (sentdex)
# Method to calculate where in the screen is the bounding box (generated from aakash) and calculate corrective outputs
# Method to calculate corrective action to take from Jack's outputs
# Method to keep the player on track for a global path goal - Jack
# Method to keep player on track for local path goal - Aakash
from capture_frame import CaptureFrame
from game_input import Keys
import time
from navigation import calculate_navigation_error

class Engine:

    def __init__(self) -> None:
        self.screen_capture = CaptureFrame((0,0,1920,1080))
        self.input_controller = Keys()
        self.mouse_movement_steps = 100
        self.navigation_error_list = []

    def _calculate_movement_steps(self, x:float,y:float) -> tuple:
        movement_time = 1 # in seconds
        dt = movement_time/self.mouse_movement_steps
        dx = x/self.mouse_movement_steps
        dy = y/self.mouse_movement_steps
        return dx,dy,dt

    def move_mouse(self, mouse_button=None, mouse_movement=None, duration:float = 0.5) -> None:
        if mouse_button is not None:
            self.input_controller.directMouse(buttons=mouse_button[0])
            time.sleep(duration)
            self.input_controller.directMouse(buttons=mouse_button[1])
        
        if mouse_movement is not None:
            move_x, move_y, move_t = self._calculate_movement_steps(mouse_movement[0],mouse_movement[1])
            for i in range(0,self.mouse_movement_steps):
                self.input_controller.directMouse(int(move_x), int(move_y))
                time.sleep(move_t)

    def keyboard_press(self, keyboard_button:str) -> None:
        self.input_controller.directKey(keyboard_button)
    
    def keyboard_release(self, keyboard_button:str) -> None:
        self.input_controller.directKey(keyboard_button, self.input_controller.key_release)


    def get_navigation_error(self):
        current_error = calculate_navigation_error(self.screen_capture.get_current_frame(),True)
        self.navigation_error_list.append(current_error)
        print(self.navigation_error_list)

    def runner(self):
        for i in range(0,200):
            self.get_navigation_error()