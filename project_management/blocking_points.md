# Blocking points, conflicts and lessons learned

## Technical blocking points

### 1. Building our own renderer (weeks 1 – 3)

The "MLX-like functions only" rule meant we could not just use a game framework's sprite
and drawing helpers. We started with CPU drawing (`put_pixel`, `put_line`, `put_polygon`
with numpy) and quickly saw it would be too slow, so we moved to a **GPU renderer with
moderngl** (2026-09-10, "now using only gpu renderer" on 2026-09-15).

- **Blocked on**: images not showing (commit of 2026-09-16), alpha blending, anti-aliasing
  creating artifacts (2026-10-02: *"disable AA style bug, (it wasnt AA)"*), font blending
  (2026-10-20).
- **Solved by**: reading the moderngl / OpenGL documentation, isolating each shader, and
  ping-pong framebuffers to apply color operations.
- **Cost**: about 3 weeks before the first maze was on screen, but every screen after that
  was built from the same meshes.

### 2. Circular imports (weeks 5 – 7)

Entities need the level, the level needs entities, UI needs both, and textures are needed
everywhere. Python raised `ImportError` on partially initialised modules several times.

- **Solved by**: `TYPE_CHECKING` imports for type hints, imports inside methods when needed,
  and the `App` dataclass that carries the shared services instead of importing them.

### 3. Ghost movement and A\* (week 5)

Ghosts were stuck, oscillated, or cut through walls: the move cache was not invalidated
on a new maze, and the wall filter in `get_possible_moves` was wrong.

- **Solved by**: rewriting A\* with a binary heap and a tie-breaker, fixing the filter,
  invalidating the cache on generation, and adding the *Wall Hack* cheat that draws each
  ghost's path — which also became a debugging tool.

### 4. mypy and flake8 at scale (week 7)

When the CI was added (2026-10-20) a lot of errors appeared at once.

- **Solved by**: one dedicated clean-up day (2026-10-21, *"almost all mypy errors fixed"*),
  then CI on every PR so it never piled up again.

### 5. Performance of the UI (week 8)

With all menus in the mesh tree, hover detection and mesh iteration caused lag.

- **Solved by**: optimising `_iter_meshes`, only searching clickables once, skipping hidden
  interfaces.

### 6. Resizable window and fullscreen (weeks 9 – 10)

Mouse positions were wrong on a scaled window and the window kept "ghosting" when going
from fullscreen back to windowed.

- **Solved by**: translating the mouse position with the scaling mode, and fixing the
  switch between fullscreen and windowed mode.

### 7. Release pipeline (week 10)

The release workflow failed twice on 2026-11-11: `glcontext` had no prebuilt wheel for the
default runner Python, and GitHub Releases refused a release without a tag.

- **Solved by**: pinning Python 3.13 in the workflow and giving each release its own tag.

## Organisational blocking points

### Menus came late

The ring progression system (our own addition) took most of weeks 6 – 8. As a result all
menus (lobby, victory, game over, how to play, leaderboard, settings) were built in the last
10 days. The Figma mockups and the shared `Button` widget made this possible, but the full
game loop (menu → game → highscore → menu) was only connected on 2026-11-09.

**Lesson:** build a minimal version of every screen early, then improve it.

### Merge conflicts

Working on separate areas kept conflicts rare, but some happened on shared files
(`game.py`, `config_model.py`, interfaces) — for example on 2026-10-14 (*"merge error, double
import"*) and 2026-10-27 (*"merge conflicts"*). They were fixed by the author of the PR,
together when the conflict touched the other teammate's code.

**Lesson:** merge `main` into long branches often; keep shared files small.
