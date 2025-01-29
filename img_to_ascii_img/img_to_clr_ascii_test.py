from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import string
import os
import random
import uuid

# Usamos os caracteres imprimíveis da biblioteca string
ASCII_CHARS = "@#$%8&WM*oahkbdpqwmZOQLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'."
fonts_dir = r"C:\Windows\Fonts"
monospaced_fonts = [
    "consola.ttf",
    "cour.ttf",
    "courbd.ttf",
    "lucon.ttf",
    "dejavusansmono.ttf"
]

fonts = [os.path.join(fonts_dir, font) for font in monospaced_fonts if os.path.exists(os.path.join(fonts_dir, font))]
fonts.extend([os.path.join('fonts', font) for font in os.listdir(os.path.join(os.path.dirname(__file__),'fonts'))])


def resize_image(image, new_width=100):
    """Redimensiona a imagem proporcionalmente."""
    width, height = image.size
    new_height = int(new_width * (height / width))
    resized_image = image.resize((new_width, new_height))
    return resized_image


def adjust_brightness(image, factor=1.5):
    """Ajusta o brilho da imagem."""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def normalize_brightness(pixels):
    """Normaliza os valores de brilho para melhorar os detalhes."""
    brightness_values = [int((rgb[0] + rgb[1] + rgb[2]) / 3) for rgb in pixels]
    min_brightness = min(brightness_values)
    max_brightness = max(brightness_values)
    normalized_pixels = [
        int(((b - min_brightness) / (max_brightness - min_brightness)) * 255)
        for b in brightness_values
    ]
    return normalized_pixels


def generate_ascii_image(image, chosed_font, font_size):
    """Gera uma imagem ASCII colorida."""
    # Define o tamanho dos caracteres na nova imagem
    char_width = 10
    char_height = 18  # Altura e largura aproximada de uma fonte monoespaçada

    font = ImageFont.truetype(chosed_font, font_size)

    # Calcula o tamanho da nova imagem
    new_width, new_height = image.size
    output_width = new_width * char_width
    output_height = new_height * char_height

    # Cria a nova imagem vazia
    ascii_image = Image.new("RGB", (output_width, output_height), "black")
    draw = ImageDraw.Draw(ascii_image)

    # Itera pelos pixels da imagem original
    pixels = list(image.getdata())
    brightness_values = normalize_brightness(pixels)
    num_chars = len(ASCII_CHARS)

    for y in range(new_height):
        for x in range(new_width):
            # Obtém o índice do pixel
            pixel_index = y * new_width + x
            r, g, b = pixels[pixel_index][:3]  # Obtém o RGB do pixel
            brightness = brightness_values[pixel_index]
            char_index = int(
                (brightness / 255) * (num_chars - 1)
            )  # Escala para o conjunto de caracteres
            char = ASCII_CHARS[char_index]  # Escolhe o caractere correspondente

            # Calcula a posição para desenhar o caractere
            position = (x * char_width, y * char_height)

            # Desenha o caractere na imagem com a cor do pixel original
            draw.text(position, char, fill=(r, g, b), font=font)

    return ascii_image


def convert(image_path, output_path):
    """Converte uma imagem em ASCII colorido e salva como nova imagem."""
    try:
        image = Image.open(image_path)
        image = adjust_brightness(image, factor=1.5)  # Aumenta o brilho
        image = resize_image(image, new_width=100)  # Ajusta a largura desejada
        font_sizes = (14,25,40,50,100,110) #50,25,100,110
        #font_size = 100
        lfilename = f'{uuid.uuid4()}'
        for font_size in font_sizes:
            ascii_image = generate_ascii_image(image, os.path.join(os.path.dirname(__file__), "fonts", "FiraCode-Bold.ttf"), font_size)

            # Salva a nova imagem
            filename = f'{lfilename} - {font_size}.jpg'
            ascii_image.save(output_path+filename)
            print(f"Imagem ASCII colorida salva em: {output_path}{filename}")
        os.remove(image_path)
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")


if __name__ == "__main__":
    # Exemplo de uso
    input_image_path = 'src/' + os.listdir('src')[0]  # Caminho da imagem de entrada
    output_image_path = "output/image/"  # Caminho da saída
    convert(input_image_path, output_image_path)
