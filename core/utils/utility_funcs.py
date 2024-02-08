# draw dashed line
import settings as sts
import pygame as pg


def draw_dashed_line():

    dash_length = 90  # Length of each dash
    gap_length = 25    # Length of each gap
    total_segments = (sts.WINDOW_HEIGHT - 30) // (dash_length +
                                                  gap_length)  # Calculate total segments
    remaining_gap = sts.WINDOW_HEIGHT - 30 - total_segments * \
        (dash_length + gap_length)  # Calculate remaining gap

    y = 15  # Initial y-coordinate
    for _ in range(total_segments):
        pg.draw.line(pg.display.get_surface(), sts.COLOR_MAP_LINES, (sts.WINDOW_WIDTH // 2, y),
                     (sts.WINDOW_WIDTH // 2, y + dash_length), 2)
        y += dash_length + gap_length

    # Draw the remaining gap at the bottom
    pg.draw.line(pg.display.get_surface(), sts.COLOR_MAP_LINES, (sts.WINDOW_WIDTH // 2, y),
                 (sts.WINDOW_WIDTH // 2, y + remaining_gap), 2)


def render_text_with_outline(font, text, color, outline_color, outline_width):
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()

    outline_surface = pg.Surface(
        (text_width + 2 * outline_width, text_height + 2 * outline_width), pg.SRCALPHA)

    # Render the outline text
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surface.blit(font.render(
                    text, True, outline_color), (dx, dy))

    # Render the main text on top
    outline_surface.blit(text_surface, (0, 0))

    return outline_surface
