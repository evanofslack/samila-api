import matplotlib.colors as colors
from equations import combos
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from samila import GenerativeImage
from samila.functions import save_fig_buf
from samila.params import VALID_COLORS, Projection

router = APIRouter(
    tags=["image"],
)


@router.get("/image", responses={200: {"content": {"image/png": {}}}})
async def generative_image(
    eq: int | None = None,
    proj: str | None = None,
    color: str | None = None,
    bg: str | None = None,
):
    """
    Generate image with Samila
    """

    print(eq, proj, color, bg)

    # EQUATIONS
    f1, f2 = None, None
    if eq != None:
        try:
            f1, f2 = combos[eq]
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

    g = GenerativeImage(f1, f2)
    g.generate()
    g.plot(projection=p, color=c, bgcolor=b)

    resp = save_fig_buf(g.fig)
    if not resp["status"]:
        print("Could not save image to buffer")
        return None

    buffer = resp["buffer"]
    buffer.seek(0)
    return StreamingResponse(content=buffer, media_type="image/png")
