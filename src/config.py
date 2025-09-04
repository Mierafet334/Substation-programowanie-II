# Config class for loading/writing user settings, defaults and storing game constants.

class Config():
    # Public constants
    REGION_SIZE : int = 16 # Used also in geometry shader, no auto update
    TILE_SIZE : int = 16 # Used also in geometry shader, no auto update
    FOV_MIN : float = 15.0
    FOV_MAX : float = 60.0
    SCROLL_MIN : float = 1.0
    SCROLL_MAX : float = 10.0
    CAMERA_DEFAULT_FOV : float = 53.13
    CAMERA_Z_NEAR : float = 0.1
    CAMERA_Z_FAR : float = 10.0
    CAMERA_SPEED_DEFAULT : float = 0.0005
    REGION_Z_DEPTH : float = 2.0
    DEFAULT_WORLD_SIZE : int = 3
    GUI_BUILD_MENU_WIDTH : int = 400
    GUI_BUILD_MENU_HEIGHT : int = 300
    GUI_BUILD_MENU_TOOLTIP_WIDTH : int = 300
    GUI_BUILD_MENU_TOOLTIP_HEIGHT : int = 50
    PLAYER_START_MONEY : float = 3000.0