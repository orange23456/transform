import importlib.util as u
mods = ['pytesseract', 'easyocr', 'paddleocr', 'cv2', 'PIL', 'numpy']
print({m: bool(u.find_spec(m)) for m in mods})
