import qrcode
from qrcode.main import QRCode
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
)


def image_as_bytes(image):
    stream = BytesIO()
    image.save(stream)
    return stream.getvalue()


class QR41C:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        version = kwargs.get("version")
        if version != 1 <= version <= 40:
            self.version = 1
        else:
            self.version = version

        self.error_correction = self.module_corrector_mapping[kwargs.get("error_correction")]
        self.box_size = kwargs.get("box_size")
        self.border = kwargs.get("border")
        self.image_factory = self.image_factory_mapping[kwargs.get("image_factory")]

        mask_pattern = kwargs.get("mask_pattern")
        if mask_pattern != 0 <= mask_pattern <= 7:
            self.mask_pattern = None
        else:
            self.mask_pattern = mask_pattern

        self.module_drawer = self.module_drawer_mapping[kwargs.get("module_drawer")]()

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

    def make(self, data):
        qr = QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
            image_factory=self.image_factory,
            mask_pattern=self.mask_pattern,
        )

        if data is None:
            raise ValueError("Данные не были переданы")

        qr.add_data(data)
        image = qr.make_image(module_drawer=self.module_drawer)
        return image_as_bytes(image)


if __name__ == "__main__":
    qr = QR41C(
        version=1,
        error_correction=0,
        box_size=10,
        border=4,
        image_factory=0,
        mask_pattern=0,
        module_drawer=0
    )
    print(qr.make("Hello, World!"))