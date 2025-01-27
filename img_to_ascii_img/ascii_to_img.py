from PIL import Image, ImageDraw, ImageFont
from sys import argv
import os


def txt_to_image(
    txt_file_path,
    output_image_path,
    font_path=None,
    font_size=20,
    bg_color=(0, 0, 0),
    text_color=(255, 255, 255),
):
    try:
        # Leia o conteúdo do arquivo .txt
        with open(txt_file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Configurar a fonte (usar uma fonte monoespaçada)
        if font_path is None:
            font_path = r"C:\Windows\Fonts\consola.ttf"  # Fonte Consolas no Windows
        font = ImageFont.truetype(font_path, font_size)

        # Calcular o tamanho da imagem baseado no texto
        lines = text.splitlines()
        max_line_width = max(
            [font.getbbox(line)[2] for line in lines]
        )  # Largura da linha mais longa
        line_height = font.getbbox("A")[3]  # Altura de uma linha
        image_width = max_line_width + 20  # Margem horizontal
        image_height = line_height * len(lines) + 20  # Margem vertical

        # Criar uma imagem em branco
        image = Image.new("RGB", (image_width, image_height), color=bg_color)
        draw = ImageDraw.Draw(image)

        # Desenhar o texto na imagem
        y = 10  # Margem superior
        for line in lines:
            draw.text((10, y), line, font=font, fill=text_color)
            y += line_height

        # Salvar a imagem
        image.save(output_image_path)
        os.remove(txt_file_path)
        print(f"Imagem salva em: {output_image_path}")

    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")


# Exemplo de uso
for image in os.listdir("./output/ascii"):
    output_image = f"{image}.jpg"
    txt_to_image(
        os.path.join("./output", "ascii", image),
        os.path.join("./output", "image", output_image),
    )
