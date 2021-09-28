from pyvarml.utils.images import Images

foo = Images("path/to/image") # Change here

foo.convert_rgb_to_gray_scale(100, 100, False)

print(f"Shape: {foo.converted.shape}")
