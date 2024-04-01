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

    def make(self, *args, **kwargs):
        version = kwargs.get("version", 0)
        if version is not None and not 1 <= version <= 40:
            version = None

        mask_pattern = kwargs.get("mask_pattern", 0)
        if mask_pattern is not None and not 0 <= mask_pattern <= 7:
            mask_pattern = None

        qr = QRCode(
            version=version,
            error_correction=self.module_corrector_mapping[kwargs.get("error_correction", 0)],
            box_size=kwargs.get("box_size", 10),
            border=kwargs.get("border", 4),
            image_factory=self.image_factory_mapping[kwargs.get("image_factory", 0)],
            mask_pattern=mask_pattern,
        )
        data = args[0]
        if data is None:
            raise ValueError("Данные не были переданы")

        qr.add_data(data)
        image = qr.make_image(module_drawer=self.module_drawer)
        return image_as_bytes(image)
