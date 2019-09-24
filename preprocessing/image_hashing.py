#perceptual image hashing found on Quora by Vladislav Zorov

from PIL import Image, ImageStat

def hash_image(image_path):
    """open image from image_path, resize then upscale using lanczos followed by
    conversion to black and white (similar to convolution).
    
    Next, the mean of the global statistic of the image is calculated using ImageStat.Stat

    Lastly, the sequence data is flattened then the vector is iterated and compared with the mean
    if the value is greater than the mean, then 2**i, which is then summed and returned
    """
    img = Image.open(image_path).resize((8,8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if pic > mean else 0) << i for i, pic in enumerate(img.getdata()))