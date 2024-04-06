# Color Display Pattern Generator Project

This project is designed to display colors and images on a screen controlled by a Raspberry Pi or Windows PC via serial communication. It uses Pygame library to create a graphical interface and handles incoming commands from the serial port to change colors and display images.

## Requirements

- Python 3.x
- Pygame library
- Serial library (already included in Python standard library)

## Setup

1. Clone the repository:

git clone https://github.com/your-username/color-display-project.git

2. Install the required libraries:
```console
pip install pygame
```
3. Connect your Raspberry Pi or Windows PC to the display screen via serial port.

## Usage

1. Run the main script or double click the batch file:

```console
python PAT_V01.py.py
```
2. Use the following serial commands to interact with the display:

- F1 [color_index]: Change the display color. color_index is a number from 1 to n, where n is the total number of colors defined in the config.ini file.
- F2: Toggle fullscreen mode.

3. Use the following keyboard or mouse click to interact with the display:
- mouse left click : change the next pattern.
- Q: Quit the program.
## Configuration

You can customize the colors and image paths by editing the config.ini file. Here is an example of the config.ini file:

```ini
[colors]
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
PIC = 0
pic1 = 0,
square1 = 0,
green1 = 0, 255, 0
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
