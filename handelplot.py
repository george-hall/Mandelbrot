

"""
Plot the Mandelbrot Set.
"""


from __future__ import division

import colorsys

import Tkinter


def compute_deltas(real_axis_range, im_axis_range, window_width,
                   window_height):

    """
    Return the size of the range covered by each pixel for the x and y axes.
    I.e. 'dx' is the jump in value of the real component of the a point for
    every pixel moved in the positive x direction. 'dy' is the analaogue of
    'dx' but for the imaginary (y) axis.
    """

    dx = abs(real_axis_range[1] - real_axis_range[0]) / window_width
    dy = abs(im_axis_range[1] - im_axis_range[0]) / window_height

    return (dx, dy)


def compute_escape_iterations(current_point):

    """
    Compute the number of iterations required for this point to escape the
    Mandelbrot Set. Otherwise, return -1, signifying that the point is, in fact
    in the Set.
    """

    z_value = (0+0j)
    c_value = (current_point.real + (current_point.imag * 1j))

    for iteration_number in xrange(64):
        if z_value.real > 2 or z_value.imag > 2:
            return iteration_number
        else:
            z_value = (z_value**2) + c_value

    return -1


def colour_pixel(image, pos, colours):

    """
    Set pixel with co-ordinates given in pos to RGB colour given by colours.
    """

    h, s, v = colours
    x, y = pos

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    image.put("#%02x%02x%02x" % (r*255, g*255, b*255), (y, x))


def populate_pixel_array(image, window_width, window_height,
                         real_axis_range=(-2, 1), im_axis_range=(-1, 1)):

    """
    Populate pixels in 'image' with colours set according to how quickly each
    pixel's corresponding point escapes the Mandelbrot Set.
    """

    (dx, dy) = compute_deltas(real_axis_range, im_axis_range, window_width,
                              window_height)
    current_point = real_axis_range[0] + (im_axis_range[0] * 1j)

    for x_pixel in xrange(window_width):
        for y_pixel in xrange(window_height):
            escape_iterations = compute_escape_iterations(current_point)
            if escape_iterations != -1:
                colour_pixel(image, (y_pixel, x_pixel),
                             (escape_iterations / 64, 1, 1))
            else:
                colour_pixel(image, (y_pixel, x_pixel), (0, 0, 0))

            current_point += (dy * 1j)
        current_point = (current_point.real + dx) + (im_axis_range[0] * 1j)


def main():

    """
    Do Tkinter bootplating, and create blank image to be populated. Do this
    population and then plot the result.
    """

    root = Tkinter.Tk()

    window_width = 750
    window_height = 500

    image = Tkinter.PhotoImage(height=window_height, width=window_width)

    populate_pixel_array(image, window_width, window_height)

    label = Tkinter.Label(root, image=image)
    label.grid()

    root.iconbitmap('@images/handel_icon.xbm')
    root.title("HandelPlot")
    root.mainloop()


if __name__ == "__main__":
    main()