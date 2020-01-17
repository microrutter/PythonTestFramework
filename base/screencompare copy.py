from PIL import Image, ImageDraw


class ScreenAnalysis:

    STAGING_URL = ""
    PRODUCTION_URL = ""
    driver = None

    def __init__(self, prod, comp):
        self.screen1 = prod
        self.screen2 = comp

    def analyze(self):
        screenshot_staging = Image.open(self.screen2)
        screenshot_production = Image.open(self.screen1)
        columns = 80
        rows = 100
        screen_width, screen_height = screenshot_staging.size

        block_width = (
            (screen_width - 1) // columns
        ) + 1  # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height + 1):
            for x in range(0, screen_width, block_width + 1):
                region_staging = self.process_region(
                    screenshot_staging, x, y, block_width, block_height
                )
                region_production = self.process_region(
                    screenshot_production, x, y, block_width, block_height
                )

                if (
                    region_staging is not None
                    and region_production is not None
                    and region_production != region_staging
                ):
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle(
                        (x, y, x + block_width, y + block_height), outline="red"
                    )

        screenshot_staging.save("result.png")

    @staticmethod
    def process_region(image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 10

        for coordinate_y in range(y, y + height):
            for coordinate_x in range(x, x + width):
                try:
                    pixel = image.getpixel((coordinate_x, coordinate_y))
                    region_total += sum(pixel) / 4
                except:
                    return

        return region_total / factor
