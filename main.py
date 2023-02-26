"""
Image to ASCII art
Converts image to ASCII by mapping each pixel's luminosity to an ASCII matrix, then prints it out.
"""
from PIL import Image

IMAGE_PATH = "images/the_mona_lisa.jpeg"
ASCII_MATRIX = " .:-=+*#%@"
RGB_MAX = 255


def main() -> None:
    """
    Prints out the image in ASCII
    :rtype: None
    """
    image = Image.open(IMAGE_PATH)

    # Resized to fit a full screen terminal window.
    image = image.resize((60, 100))

    pixel_matrix = compute_pixel_matrix(image)

    for row in pixel_matrix:
        for character in row:
            # Print character 3 times to account for image squash
            print(character * 3, end="")
        print()


def calculate_pixel_luminosity(red: int, green: int, blue: int) -> int:
    """Returns pixel luminosity
    Calculates and returns the pixel luminosity by forming a weighted average to account for
    human perception, using this formula-

    |
    |    L = 0.2126 R + 0.7152 G + 0.0722 B
    |

    Since humans are more sensitive to green light, it is weighted the most heavily, followed
    by red, then blue. This helps in deciding what character to use.

    :param red: The R value
    :type red: int
    :param green: The G value
    :type green: int
    :param blue: The B value
    :type blue: int
    :returns: The pixel luminosity based on the passed in R, G, B values
    :rtype: int
    """
    return round((0.2126 * red) + (0.7152 * green) + (0.0722 * blue))


def compute_ascii_character_map(pixel_luminosity: int, maximum_luminosity: int) -> str:
    """Returns ASCII character based on luminosity
    Computes ASCII character based on the luminosity percentage, multiplied the length of the
    ASCII matrix, subtracted by 1 (to account for the index) to get the index of the character
    to map to.

    |
    map_index = ( (pixel_luminosity / maximum_luminosity) * length of ASCII matrix ) - 1


    :param pixel_luminosity:
    :type pixel_luminosity: int
    :param maximum_luminosity:
    :type maximum_luminosity: int
    :returns: The ASCII character the luminosity maps to
    :rtype: str
    """
    ascii_map_index = round((pixel_luminosity / maximum_luminosity) * len(ASCII_MATRIX)) - 1
    return ASCII_MATRIX[ascii_map_index]


def compute_pixel_matrix(image) -> list[list[str]]:
    """Returns pixel matrix mapped to ASCII characters
    Takes a PIL.Image object, goes through each of the pixels, maps the pixel's RGB values to
    an ASCII character, storing in a 2D array, using the above functions.

    :param image:
    :returns: The pixel matrix (2D array) mapped to ASCII characters
    :rtype: list[list[str]]
    """
    pixel_matrix = []
    maximum_luminosity = calculate_pixel_luminosity(RGB_MAX, RGB_MAX, RGB_MAX)

    # Goes through each pixel in the image
    for i in range(image.height):
        pixel_row = []

        for j in range(image.width):
            # Gets the RGB values
            coordinates = (j, i)
            red, green, blue = image.getpixel(coordinates)

            # Calculates pixel luminosity
            pixel_luminosity = calculate_pixel_luminosity(red, green, blue)

            # Maps luminosity to ASCII
            character_map = compute_ascii_character_map(pixel_luminosity, maximum_luminosity)

            pixel_row.append(character_map)

        pixel_matrix.append(pixel_row)

    return pixel_matrix


if __name__ == '__main__':
    main()
