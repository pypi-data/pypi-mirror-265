from typing import Type, Optional
import qrcode
from qrcode.main import QRCode, GenericImage
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
    with BytesIO() as output:
        image.save(output, format="PNG")
        return output.getvalue()


class QR41C:
    module_drawer: StyledPilQRModuleDrawer
    module_corrector: int
    data: str
    version: int
    box_size: int
    border: int
    mask_pattern: int
    image_factory: Optional[Type[GenericImage]]

    def __init__(self, *args, **kwargs):
        self.module_drawer = self.module_drawer_mapping.get(kwargs.get("module_drawer", 0))()
        self.module_corrector = self.module_corrector_mapping.get(kwargs.get("module_corrector", 0))
        self.data = kwargs.get("data", "")
        self.version = kwargs.get("version", 1)
        self.box_size = kwargs.get("box_size", 10)
        self.border = kwargs.get("border", 4)
        self.mask_pattern = kwargs.get("mask_pattern", 0)
        self.image_factory = self.image_factory_mapping.get(kwargs.get("image_factory", 0))

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

    def make(self):
        qr = QRCode(
            version=self.version,
            error_correction=self.module_corrector,
            box_size=self.box_size,
            border=self.border,
            mask_pattern=self.mask_pattern,
            image_factory=self.image_factory
        )

        qr.add_data(self.data)
        image = qr.make_image(module_drawer=self.module_drawer)
        return image_as_bytes(image)
