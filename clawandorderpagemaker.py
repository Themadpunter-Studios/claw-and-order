from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import os

def draw_crop_marks(c, x, y, card_width, card_height, mark_length=0.1 * inch):
    # Top-left
    c.line(x - mark_length, y, x, y)
    c.line(x, y - mark_length, x, y)
    # Top-right
    c.line(x + card_width, y - mark_length, x + card_width, y)
    c.line(x + card_width, y, x + card_width + mark_length, y)
    # Bottom-left
    c.line(x - mark_length, y + card_height, x, y + card_height)
    c.line(x, y + card_height, x, y + card_height + mark_length)
    # Bottom-right
    c.line(x + card_width, y + card_height, x + card_width + mark_length, y + card_height)
    c.line(x + card_width, y + card_height, x + card_width, y + card_height + mark_length)

def generate_image_card_pdf(input_file, output_file):
    card_width = 2.5 * inch
    card_height = 3.5 * inch

    # Absolute path to where this script is
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cards_folder = os.path.join(script_dir, "cards")

    # Read card names
    with open(input_file, 'r') as f:
        cards = [line.strip() for line in f if line.strip()]

    c = canvas.Canvas(output_file, pagesize=letter)
    page_width, page_height = letter

    cards_per_row = 3
    cards_per_col = 3
    max_cards_per_page = cards_per_row * cards_per_col

    # Center grid on page
    total_grid_width = cards_per_row * card_width
    total_grid_height = cards_per_col * card_height
    x_offset = (page_width - total_grid_width) / 2
    y_offset = (page_height - total_grid_height) / 2

    for i, card_name in enumerate(cards):
        page_card_index = i % max_cards_per_page
        row = page_card_index // cards_per_row
        col = page_card_index % cards_per_row

        x = x_offset + col * card_width
        y = y_offset + (cards_per_col - 1 - row) * card_height  # bottom-left origin

        image_path = os.path.join(cards_folder, f"{card_name}.png")
        if os.path.exists(image_path):
            try:
                img = ImageReader(image_path)
                c.drawImage(img, x, y, width=card_width, height=card_height, preserveAspectRatio=True, anchor='c')
            except Exception as e:
                print(f"Error loading image '{image_path}': {e}")
        else:
            print(f"Warning: Image file '{image_path}' not found. Leaving blank space.")

        # Draw crop marks
        draw_crop_marks(c, x, y, card_width, card_height)

        # New page if needed
        if (page_card_index == max_cards_per_page - 1) or (i == len(cards) - 1):
            c.showPage()

    c.save()
    print(f"PDF saved to: {output_file}")

# === Run ===
if __name__ == "__main__":
    generate_image_card_pdf("cards.txt", "output_cards_portrait.pdf")
