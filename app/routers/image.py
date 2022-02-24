from cProfile import label

import matplotlib.colors as colors
import matplotlib.font_manager
import matplotlib.pyplot as plt
from equations import combos
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from samila import GenerativeImage
from samila.functions import save_fig_buf
from samila.params import VALID_COLORS, Projection

matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")[:10]
font_dir = ["/Users/evan/Downloads/Montserrat"]
for font in matplotlib.font_manager.findSystemFonts(font_dir):
    matplotlib.font_manager.fontManager.addfont(font)

router = APIRouter(
    tags=["image"],
)


@router.get("/image", responses={200: {"content": {"image/png": {}}}})
async def generative_image(
    eq: int | None = None,
    proj: str | None = None,
    color: str | None = None,
    bg: str | None = None,
    seed: int | None = None,
    text: str | None = None,
    loc: str | None = None,
):
    """
    Generate image with Samila
    """

    print(eq, proj, color, bg, seed)

    # EQUATIONS
    f1, f2 = None, None
    if eq != None:
        try:
            f1, f2 = combos[eq]
            print(f1, f2)
        # Out of range of defined combos
        except IndexError:
            pass

    # PROJECTION
    p = None
    if proj != None:
        for x in Projection:
            if proj.lower() == x.value:
                p = x
                break
        else:
            print("projection not found")

    # COLOR
    c = None
    if color != None:
        if isinstance(color, str) and color in VALID_COLORS:
            c = color
        elif isinstance(color, str):
            try:
                c = colors.hex2color(f"#{color}")
            except Exception as e:
                print(e)
                print(f"{color} is an invalid color")

    # BACKGROUND COLOR
    b = None
    if bg != None:
        if isinstance(bg, str) and bg in VALID_COLORS:
            b = bg
        elif isinstance(bg, str):
            try:
                b = colors.hex2color(f"#{bg}")
            except Exception as e:
                print(e)
                print(f"{bg} is an invalid color")

    # SEED
    s = None
    if seed != None:
        s = seed

    # GENERATE IMAGE
    g = GenerativeImage(f1, f2)
    g.generate(seed=s)
    g.plot(projection=p, color=c, bgcolor=b)

    # TEXT

    if text != None:
        plt.legend(frameon=False)
        plt.text(
            # 10,
            # 10,
            0.05,
            0.9,
            text,
            color="white",
            fontsize=48,
            # ha="",
            # va="top",
            transform=g.fig.transFigure,
            fontweight=700,
            fontstretch=100,
            fontfamily="montserrat",
        )

    # WRITE BINARY IMAGE
    resp = save_fig_buf(g.fig)
    if not resp["status"]:
        print("Could not save image to buffer")
        return None
    buffer = resp["buffer"]
    buffer.seek(0)

    # ADD SEED AS HEADER
    headers = {"X-Seed": str(g.seed)}

    return StreamingResponse(content=buffer, headers=headers, media_type="image/png")
