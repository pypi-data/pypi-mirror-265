from typing import Type, Optional
import qrcode
from qrcode.main import GenericImage, QRCode
from io import BytesIO
from qrcode.image.pil import PilImage
from qrcode.image.pure import PyPNGImage
from qrcode.image.svg import SvgFragmentImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
    StyledPilQRModuleDrawer
)


def image_as_bytes(image):
    stream = BytesIO()
    image.save(stream)
    return stream.getvalue()


class QR41C:
    module_drawer: StyledPilQRModuleDrawer
    module_corrector: int
    data: str
    version: int
    box_size: int
    border: int
    mask_pattern: int
    image_factory: Optional[Type[GenericImage]]

    def __init__(self):
        self.module_drawer = SquareModuleDrawer()
        self.module_corrector = qrcode.constants.ERROR_CORRECT_L
        self.version = 1
        self.box_size = 10
        self.border = 4
        self.mask_pattern = 0
        self.image_factory = PilImage

    module_drawer_mapping = {
        0: SquareModuleDrawer,  # сплошной
        1: RoundedModuleDrawer,  # закругленный
        2: GappedSquareModuleDrawer,  # с промежутками
        3: CircleModuleDrawer,  # круглый
        4: VerticalBarsDrawer,  # вертикальные полосы
        5: HorizontalBarsDrawer,  # горизонтальные полосы
    }

    module_corrector_mapping = {
        0: qrcode.constants.ERROR_CORRECT_L,  # 7%
        1: qrcode.constants.ERROR_CORRECT_M,  # 15%
        2: qrcode.constants.ERROR_CORRECT_Q,  # 25%
        3: qrcode.constants.ERROR_CORRECT_H,  # 30%
    }

    image_factory_mapping = {
        0: PilImage,
        1: PyPNGImage,
        2: SvgFragmentImage,
        3: StyledPilImage
    }

    def test(self):
        return False

    def make(self, data):
        qr = QRCode()
        qr.add_data(data)
        image = qr.make_image()
        return image_as_bytes(image)
