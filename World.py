import pygame

def import_screen(filename: str, coords: tuple):
    with open(f'leveldat/{filename}') as f:
        contents = f.read()
        print(contents)