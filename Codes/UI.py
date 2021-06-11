from pygvisuals import widgets
from pygvisuals import borders


def get_skill_buttons(character, x, y):
    res = []
    skill_list = character.get_skills()
    for i in range(0, len(skill_list)):
        button = widgets.button.Button(x + 40 * i, y, 400, 100, text=skill_list[i], callback=here)
        button.setActive(True)
        button.setVisible(True)
        button.setHoveredOverlay((100, 0, 0))
        button.setPressedOverlay((0, 100, 0))
        button.setBackground((0, 0, 100))
        res.append(button)
    return res


def here():
    print('here')
