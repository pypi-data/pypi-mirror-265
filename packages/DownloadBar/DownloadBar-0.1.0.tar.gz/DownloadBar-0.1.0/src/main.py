import sys
import time

# ANSI escape codes for color formatting and graphics
COLOR_GREEN = "\033[92m"  # Green color for completed progress
COLOR_YELLOW = "\033[93m"  # Yellow color for moderate progress
COLOR_RED = "\033[91m"  # Red color for low progress
COLOR_RESET = "\033[0m"   # Reset color to default
GRAPHICS_BLOCKS = "▮"  # Unicode block character for progress indication
GRAPHICS_SPACES = "░"  # Unicode block character for remaining space

def get_progress_color(progress):
    if progress >= 80:
        return COLOR_GREEN
    elif progress >= 50:
        return COLOR_YELLOW
    else:
        return COLOR_RED

def download_animation(duration):
    start_time = time.time()
    min_step = 0.02  # Minimum step size for progress calculation
    bar_width = 50   # Width of the progress bar
    while True:
        elapsed_time = time.time() - start_time
        progress = round((elapsed_time / duration) * 100)  # Round to nearest integer
        if progress >= 100 or elapsed_time >= duration:
            progress = 100
            break
        color = get_progress_color(progress)
        colored_blocks = progress * bar_width // 100  # Number of colored blocks based on progress
        remaining_blocks = bar_width - colored_blocks  # Number of remaining blocks
        progress_bar = "[" + (color + GRAPHICS_BLOCKS * colored_blocks + COLOR_RESET +
                              GRAPHICS_SPACES * remaining_blocks) + "]"
        percentage = f"{progress}%"
        sys.stdout.write(f"\rDownloading... {progress_bar} {percentage}")
        sys.stdout.flush()
        time.sleep(min_step)

    sys.stdout.write(f"\rDownloading... [{GRAPHICS_BLOCKS * bar_width}] 100%\n")
    sys.stdout.flush()
    sys.stdout.write("\nDownload complete!      \n")
    sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_animation.py <duration_in_seconds>")
    else:
        duration = float(sys.argv[1])
        download_animation(duration)
