from dataclasses import dataclass

@dataclass
class Settings:
    # Screen
    SCREEN_WIDTH: int = 1280    # Width of the game window
    SCREEN_HEIGHT: int = 720    # Height of the game window
    FPS: int = 60               # Frames per second
    TITLE: str = "I2P Final"    # Title of the game window
    DEBUG: bool = True          # Debug mode
    TILE_SIZE: int = 64         # Size of each tile in pixels
    DRAW_HITBOXES: bool = False  # Draw hitboxes for debugging
    # Audio
    MAX_CHANNELS: int = 16
    AUDIO_VOLUME: float =  0.5   # Volume of audio
    # Online
    IS_ONLINE: bool = True
    ONLINE_SERVER_URL: str = "http://localhost:8989"
    GAME_FONT = "assets/fonts/Minecraft.ttf"
    
GameSettings = Settings()