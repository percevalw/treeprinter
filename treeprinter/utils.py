from enum import Enum


class Alignment(Enum):
    START = 0,
    END = 1,
    CENTER = 2


def pad_1d(element, pad=" ", size=0, margin=(0, 0), padding=(0, 0), direction=Alignment.CENTER):
    """
    :ty
    :rtype: list of (str or list)
    :param element: The 1d-element to be padded
    :type element: (str or list)
    :param pad: The padding element to be added before and after the element
    :type pad: (str or list)
    :param size: The size of the element (without margin)
    :type size: int
    :param margin: The margin, ie the repartition of padding elements to add after of the padding
    :type margin: tuple(int, int)
    :param padding: The padding, ie the repartition of padding elements to add inside the size
    :type padding: tuple(int, int)
    :param direction: The alignment
    :type direction: Alignment
    :return: The padded element
    """
    size = max(size, len(element))
    missing = size - len(element) - padding[0] - padding[1]
    if direction == Alignment.START:
        missing_start, missing_end = 0, missing
    elif direction == Alignment.END:
        missing_start, missing_end = missing, 0
    elif direction == Alignment.CENTER:
        missing_start, missing_end = int(missing / 2), int((missing + 1) / 2)
    else:
        raise Exception("Direction should be START, END or CENTER")
    return (pad * (missing_start + padding[0] + margin[0])) + element + (pad * (missing_end + padding[1] + margin[1]))


def pad_2d(element, pad=" ", size_x=0, size_y=0, padding_x=(0, 0), margin_x=(0, 0), padding_y=(0, 0), margin_y=(0, 0),
           dir_x=Alignment.CENTER,
           dir_y=Alignment.CENTER):
    """
    :rtype: list of (str or list)
    :param element: The 2d-element to be padded
    :type element: list of (str or list)
    :param pad: The padding element to complete the element
    :type pad: (str or list)
    :param size_x: The width of the element (without margin)
    :type size_x: int
    :param size_y: The height of the element (without margin)
    :type size_y: int
    :param margin_x: The horizontal margin, ie the repartition of padding elements to add after of the padding
    :type margin_x: tuple(int, int)
    :param margin_y: The vertical margin, ie the repartition of padding elements to add after of the padding
    :type margin_y: tuple(int, int)
    :param padding_x: The horizontal padding, ie the repartition of padding elements to add inside the size
    :type padding_x: tuple(int, int)
    :param padding_y: The vertical padding, ie the repartition of padding elements to add inside the size
    :type padding_y: tuple(int, int)
    :param dir_x: The horizontal alignment
    :type dir_x: Alignment
    :param dir_y: The vertical alignment
    :type dir_y: Alignment
    :return: The padded element
    """
    size_x = max(max(map(len, element)), size_x)
    size_y = max(len(element), size_y)
    padded_lines = [pad_1d(line, pad,
                           direction=dir_x,
                           size=size_x,
                           padding=padding_x,
                           margin=margin_x)
                    for line in element]
    ret = pad_1d(padded_lines, [pad * len(padded_lines[0])],
                 direction=dir_y,
                 size=size_y,
                 padding=padding_y,
                 margin=margin_y)
    return ret


def merge_h(*elements_2d, dir_x=Alignment.CENTER, dir_y=Alignment.START):
    size_y = max(map(len, elements_2d))
    padded_elements = [pad_2d(b, size_y=size_y, padding_x=(0, 0), dir_x=dir_x, dir_y=dir_y) for b in elements_2d]
    concat_lines = zip(*padded_elements)
    return list(map("".join, concat_lines))


def merge_v(*elements_2d, dir_x=Alignment.CENTER, dir_y=Alignment.START):
    size_x = max(map(len, [e[0] for e in elements_2d]))
    padded_elements = [pad_2d(b, size_x=size_x, dir_x=dir_x, dir_y=dir_y) for b in elements_2d]
    concat_lines = [line for element in padded_elements for line in element]
    return concat_lines
