from bisect import bisect_right

from moderngl import Texture

from .animation import Animation
from .texture_frame import TextureFrame


class AnimationPlayer:
    anim: Animation
    time: float
    speed: float
    playing: bool

    _frames: list[TextureFrame]
    _ends: list[float]
    _total: float

    def __init__(
        self,
        animation: Animation,
        *,
        autoplay: bool = True,
        speed: float = 1.0,
    ) -> None:
        self.anim = animation
        self.speed = speed
        self.playing = autoplay
        self.time = 0.0

        self._frames = []
        self._ends = []
        self._total = 0.0
        self._build()

    @staticmethod
    def _flatten(anim: Animation) -> list[tuple[TextureFrame, float]]:
        items: list[tuple[TextureFrame, float]] = []
        for f in anim.frames:
            if isinstance(f, Animation):
                items.extend(AnimationPlayer._flatten(f))
            else:
                items.append((f, f.duration))

        total = sum(d for _, d in items)
        if total > 0 and anim.duration > 0:
            k = anim.duration / total
            items = [(f, d * k) for f, d in items]
        return items

    def _build(self) -> None:
        t = 0.0
        for frame, d in self._flatten(self.anim):
            t += d
            self._frames.append(frame)
            self._ends.append(t)
        self._total = t

    def play(self) -> None:
        if self.finished:
            self.time = 0.0
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def stop(self) -> None:
        self.playing = False
        self.time = 0.0

    def restart(self) -> None:
        self.time = 0.0
        self.playing = True

    def seek(self, t: float) -> None:
        if self._total <= 0:
            self.time = 0.0
        elif self.anim.loop:
            self.time = t % self._total
        else:
            self.time = max(0.0, min(t, self._total))

    def update(self, dt: float) -> None:
        if not self.playing or self._total <= 0:
            return

        self.time += dt * self.speed

        if self.anim.loop:
            self.time %= self._total
        elif self.time >= self._total:
            self.time = self._total
            self.playing = False

    @property
    def duration(self) -> float:
        return self._total

    @property
    def finished(self) -> bool:
        return not self.anim.loop and self.time >= self._total

    @property
    def frame(self) -> TextureFrame:
        idx = bisect_right(self._ends, self.time)
        return self._frames[min(idx, len(self._frames) - 1)]

    @property
    def texture(self) -> Texture:
        return self.frame.texture
