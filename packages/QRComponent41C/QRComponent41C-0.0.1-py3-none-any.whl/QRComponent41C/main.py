import qrcode
from qrcode.main import QRCode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)
from io import BytesIO


def image_as_bytes(image):
    with BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()


def make_pil_image_qrcode(data, module_drawer):
    qr = QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr.add_data(data)
    image = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer)
    return image_as_bytes(image)


def make_square_qrcode(data):
    return make_pil_image_qrcode(data, SquareModuleDrawer())


def make_rounded_qrcode(data):
    return make_pil_image_qrcode(data, RoundedModuleDrawer())


def make_gapped_square_qrcode(data):
    return make_pil_image_qrcode(data, GappedSquareModuleDrawer())


def make_circle_qrcode(data):
    return make_pil_image_qrcode(data, CircleModuleDrawer())


def make_vertical_bars_qrcode(data):
    return make_pil_image_qrcode(data, VerticalBarsDrawer())


def make_horizontal_bars_qrcode(data):
    return make_pil_image_qrcode(data, HorizontalBarsDrawer())
