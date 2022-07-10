import os


def remove_pie_image() -> None:
    """
    Удаляет диаграмму с указанным именем файла
    """
    try:
        os.remove('pie.jpeg')    
    except FileNotFoundError:
        print('Файла с текущим именем не существует')
