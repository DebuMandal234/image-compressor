from flask import Flask, request, jsonify
from PIL import Image, ExifTags
import io
import base64

app = Flask(__name__)

def correct_image_orientation(img):
    try:
        exif = img._getexif()
        if exif is not None:
            for orientation in exif:
                if ExifTags.TAGS.get(orientation) == 'Orientation':
                    orientation_value = exif[orientation]
                    if orientation_value == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation_value == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation_value == 8:
                        img = img.rotate(90, expand=True)
                    break
    except (AttributeError, KeyError, IndexError, TypeError):
        # Skip correction if EXIF data is not available
        pass
    return img

@app.route('/compress', methods=['POST'])
def compress_image():
    data = request.get_json()
    if not data or 'base64Array' not in data:
        return jsonify({'error': 'No base64 array provided.'}), 400

    base64_array = data['base64Array']
    compressed_images = []

    for base64_str in base64_array:
        if base64_str is None:
            compressed_images.append(None)
            continue

        try:
            # Decode the base64 string to an image
            img_data = base64.b64decode(base64_str)
            img = Image.open(io.BytesIO(img_data))

            # Correct orientation if necessary
            img = correct_image_orientation(img)

            # Resize and compress the image
            img = img.resize((600, 800), Image.LANCZOS)
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=70)

            # Encode the compressed image to base64
            compressed_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            compressed_images.append(compressed_base64)

        except Exception as e:
            compressed_images.append({'error': str(e)})

    return jsonify({'compressedBase64Array': compressed_images})

@app.route('/log', methods=['GET'])
def log_message():
    print("Script is running...41")
    return "Script is running...41"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)














# //-------------------------------------------------------



# from flask import Flask, request, jsonify
# from PIL import Image, ExifTags
# import io
# import base64

# app = Flask(__name__)

# def correct_image_orientation(img):
#     try:
#         exif = img._getexif()
#         if exif is not None:
#             for orientation in exif:
#                 if ExifTags.TAGS.get(orientation) == 'Orientation':
#                     orientation_value = exif[orientation]
#                     if orientation_value == 3:
#                         img = img.rotate(180, expand=True)
#                     elif orientation_value == 6:
#                         img = img.rotate(270, expand=True)
#                     elif orientation_value == 8:
#                         img = img.rotate(90, expand=True)
#                     break
#     except (AttributeError, KeyError, IndexError, TypeError):
#         # Skip correction if EXIF data is not available
#         pass
#     return img

# @app.route('/compress', methods=['POST'])
# def compress_image():
#     data = request.get_json()
#     if not data or 'base64' not in data:
#         return jsonify({'error': 'No base64 string provided.'}), 400

#     try:
#         # Decode the base64 string to an image
#         img_data = base64.b64decode(data['base64'])
#         img = Image.open(io.BytesIO(img_data))

#         # Correct orientation if necessary
#         img = correct_image_orientation(img)

#         # Resize and compress the image
#         img = img.resize((500, 600), Image.LANCZOS)
#         img_io = io.BytesIO()
#         img.save(img_io, format='JPEG', quality=40)

#         # Encode the compressed image to base64
#         compressed_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
#         return jsonify({'compressedBase64': compressed_base64})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/log', methods=['GET'])
# def log_message():
#     print("Script is running...")
#     return "Script is running..."

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000)
