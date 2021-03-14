import PIL.Image

def resize_keep_ar(image, size):
    (new_w, new_h) = size
    (old_w, old_h) = image.size
    ratio = min(new_w/old_w, new_h/old_h)
    (resized_w, resized_h) = (int(ratio*old_w), int(ratio*old_h))
    result = PIL.Image.new(image.mode, size)
    result.paste(image.resize((resized_w, resized_h)), (int((new_w - resized_w) / 2), int((new_h - resized_h) / 2)))
    return result