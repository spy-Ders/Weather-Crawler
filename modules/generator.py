from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from datetime import datetime
from pyimgur import Imgur
from modules import Json

_config = Json.load("config.json")

class generator:
    def __init__(self, dt, URL, bg = (255, 255, 255), code = (0, 0, 0), path = "") -> None:

        self.dt = dt
        self.URL = URL
        self.bg = bg
        self.code = code
        self.path = path

    def generate(self):

        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(self.URL)
        qr.make(fit = True)
        img = qr.make_image(image_factory = StyledPilImage, color_mask = SolidFillColorMask(self.bg, self.code), module_drawer = RoundedModuleDrawer())
        img.save(f"{self.path}{self.dt}_output.png")

    def upload(self):

        CLIENT_ID = _config["IMGUR-TOKEN"]
        PATH = f"{self.path}{self.dt}_output.png"
        local_img = Imgur(CLIENT_ID)
        uploaded_img = local_img.upload_image(PATH, title = f"{self.URL}")
        return uploaded_img.link