import pygame


def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um unico elemento de uma spritesheet preservando transparencia."""
    sheet = pygame.image.load(local_arquivo)
    tem_alpha = bool(sheet.get_flags() & pygame.SRCALPHA)

    if tem_alpha:
        sheet = sheet.convert_alpha()
        image = pygame.Surface((width, height), pygame.SRCALPHA)
    else:
        sheet = sheet.convert()
        image = pygame.Surface((width, height))

    image.blit(sheet, (0, 0), (x, y, width, height))

    if not tem_alpha:
        cor_do_fundo = image.get_at((0, 0))
        image.set_colorkey(cor_do_fundo)

    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))

    return image
