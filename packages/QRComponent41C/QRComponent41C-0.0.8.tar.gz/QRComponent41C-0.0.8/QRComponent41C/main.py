import qrcode
from qrcode.main import QRCode
from qrcode.image.styledpil import StyledPilImage
from io import BytesIO
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

    def make(self, **kwargs):
        self.module_drawer = self.module_drawer_mapping[kwargs.get("module_drawer", 0)]()
        self.module_corrector = self.module_corrector_mapping[kwargs.get("module_corrector", 0)]
        self.data = kwargs.get("data", "")

        qr = QRCode(
            error_correction=self.module_corrector
        )

        qr.add_data(self.data)
        image = qr.make_image(image_factory=StyledPilImage, module_drawer=self.module_drawer)
        return image_as_bytes(image)
