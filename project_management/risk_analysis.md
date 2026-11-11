# Risk analysis

Probability (P) and impact (I): **L**ow, **M**edium, **H**igh.

| # | Risk | P | I | Mitigation | Status |
| --- | --- | :-: | :-: | --- | --- |
| R1 | **The assigned maze package** has a different interface than expected, bugs, or is re-installed with changes during the review | M | H | The package is never used directly: a single adapter (`Maze.generate`) turns its output into our `Tile` grid. Its wheel is kept in `lib/` and used without changes. Every error it raises is caught and reported as a `MazeGenerationError`. Level sizes are limited to 5 – 100 because it crashes on a 0×0 maze. | Done |
| R2 | **"MLX-like functions only" rule**: using a library function with no MLX equivalent makes the project fail | M | H | `pygame` is only used for the window, events and image loading. All drawing is done by our own renderer (moderngl + GLSL shaders) from basic shapes. | Done |
| R3 | **Performance**: Python + many meshes + 4 ghosts running A\* could drop below 60 FPS | M | M | GPU rendering, mesh tree, move cache in `Maze`, collisions only between neighbouring tiles, re-path only when the target changes. Fixed a lag found in `_iter_meshes` (W44). | Done |
| R4 | **Crash during the defense** (traceback = project failed) | M | H | All our errors extend `BaseError` and are caught in `__main__`; config, settings and highscores fall back to defaults; files opened with context managers; config tests with pytest. | Done |
| R5 | **Faulty config given by the reviewer** ("the game configuration will be updated during the defense") | H | H | Each key — and each field of each level — is validated on its own, an invalid value only resets itself, unknown keys are ignored, every fallback is logged. | Done |
| R6 | **Scope creep** with our extra features (ring progression, texture packs, settings) | H | M | Mandatory features first (playable core by W41), extras built on top of a working game. Menus were still pushed to the end: see [blocking_points.md](blocking_points.md). | Partly happened |
| R7 | **Merge conflicts / blocking each other** in a team of two | M | M | Split by area (engine / logic / UI / data), small branches, frequent merges into `main`. | Some conflicts, solved quickly |
| R8 | **Circular imports** in a package with many cross-references (entities ↔ level ↔ UI) | H | M | `TYPE_CHECKING` imports, local imports in methods, `App` container passed around instead of importing modules. | Done |
| R9 | **OpenGL portability** (macOS core profile, Linux drivers, school computers) | M | H | OpenGL 3.3 core profile with the forward-compatible flag (needed on macOS), resizable window with fit / crop / stretch scaling, test the packaged build on the school computers. | Done |
| R10 | **Packaging** fails or the packaged game does not find its assets | M | H | `pak-man.spec` bundles assets, shaders and the default config; `make build` can rebuild it during the review. | Done |
| R11 | **Highscore file edited by hand** or corrupted | M | L | Pydantic validation and HMAC-SHA256 signature; a bad file is ignored and replaced. | Done |
| R12 | **Not able to explain AI-assisted code** during the defense | L | H | AI only for docstrings, explanations, debugging, commit messages and docs; every result reviewed by both of us. | Done |
| R13 | **Deadline**: features not finished in time | M | H | Weekly priorities in our syncs, mandatory features before extras, documentation started before the end. | Done |
