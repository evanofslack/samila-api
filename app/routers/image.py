from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from samila import GenerativeImage
from samila.functions import save_fig_buf

router = APIRouter(
    tags=["image"],
)


@router.get("/image", responses={200: {"content": {"image/png": {}}}})
async def generative_image():
    """
    Generate image with Samila
    """
    print("Generating Image")
    g = GenerativeImage()
    g.generate()
    g.plot()

    resp = save_fig_buf(g.fig)
    if not resp["status"]:
        print("Could not save image to buffer")
        return None

    buffer = resp["buffer"]
    buffer.seek(0)
    print(type(buffer))
    print(buffer)
    return StreamingResponse(content=buffer, media_type="image/png")
