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

    module_drawer_mapping = {
        "Стандартный": SquareModuleDrawer,
        "Закругленный": RoundedModuleDrawer,
        "Разорванный": GappedSquareModuleDrawer,
        "Круглый": CircleModuleDrawer,
        "Вертикальный": VerticalBarsDrawer,
        "Горизонтальный": HorizontalBarsDrawer,
    }

    module_corrector_mapping = {
        "Маленький": qrcode.constants.ERROR_CORRECT_L,
        "Средний": qrcode.constants.ERROR_CORRECT_M,
        "Высокий": qrcode.constants.ERROR_CORRECT_Q,
        "Очень высокий": qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self, *args, **kwargs):
        self.module_drawer = self.module_drawer_mapping[kwargs.get("module_drawer", "Стандартный")]()
        self.module_corrector = self.module_corrector_mapping[kwargs.get("module_corrector", "Маленький")]

    def make(self, data):
        qr = QRCode(
            error_correction=self.module_corrector
        )
        qr.add_data(data)
        image = qr.make_image(image_factory=StyledPilImage, module_drawer=self.module_drawer)
        return image_as_bytes(image)
