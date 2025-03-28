from manim import *

class AnimatedArray(VGroup):
    def __init__(self, values, box_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        self.boxes = VGroup(*[Square().scale(0.75) for _ in values])
        self.texts = VGroup(*[Text(str(val), font_size=32) for val in values])
        for box, text in zip(self.boxes, self.texts):
            text.move_to(box.get_center())
        self.arr = VGroup(*[VGroup(b, t) for b, t in zip(self.boxes, self.texts)])
        self.arr.arrange(RIGHT, buff=0.2)
        self.add(self.arr)

    def highlight(self, indices, color=YELLOW):
        return [self.arr[i][0].animate.set_color(color) for i in indices]

    def swap(self, i, j):
        return [
            self.arr[i].animate.move_to(self.arr[j].get_center()),
            self.arr[j].animate.move_to(self.arr[i].get_center())
        ]

class SelectionSortScene(Scene):
    def construct(self):
        values = [5, 2, 9, 1, 6]
        arr = AnimatedArray(values)
        arr.move_to(ORIGIN)
        self.add(arr)
        self.wait(1)

        n = len(values)
        for i in range(n):
            min_idx = i
            # Highlight the current index
            self.play(*arr.highlight([i], color=GREEN))
            for j in range(i + 1, n):
                self.play(*arr.highlight([j], color=YELLOW))
                if values[j] < values[min_idx]:
                    min_idx = j
                self.wait(0.5)
                self.play(arr.arr[j][0].animate.set_color(WHITE))
            if min_idx != i:
                self.play(*arr.swap(i, min_idx))
                # Swap the values internally as well
                arr.arr[i], arr.arr[min_idx] = arr.arr[min_idx], arr.arr[i]
                values[i], values[min_idx] = values[min_idx], values[i]
            self.play(arr.arr[i][0].animate.set_color(GREY))
        self.wait(2)

if __name__ == "__main__":
    scene = SelectionSortScene()
    scene.render()