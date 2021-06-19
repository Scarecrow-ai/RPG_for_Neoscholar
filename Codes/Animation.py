# play() need to be called every frames when animation is play ing
class Animation:
    max_fps = 60

    # effect_sprite will be shown on character's skill_target after character's animation finfished
    def __init__(self, character, sprites, fps, effect_sprite=None):
        self.sprites = sprites
        self.character = character
        self.effect_sprite = effect_sprite
        self.fps = fps
        self.call_count = 0
        self.pic_count = 0
        self.effect_down = False

    def play(self):
        animation_done = False
        sprite_changed = False
        if self.call_count == int(Animation.max_fps / self.fps):
            self.character.change_sprites(self.sprites[self.pic_count])
            self.pic_count += 1
            self.call_count = 0
            sprite_changed = True
            if self.pic_count == len(self.sprites):
                if self.effect_sprite is not None and not self.effect_down:
                    self.pic_count -= 1
                    target = self.character.skill_target
                    target.change_sprites(self.effect_sprite)
                    self.effect_down = True
                else:
                    target = self.character.skill_target
                    target.sit()
                    self.effect_down = False
                    self.pic_count = 0
                    animation_done = True
        else:
            self.call_count += 1
        return animation_done, sprite_changed
