# Acceptance test plan

Each line is a requirement of the subject (or one of our features), how to test it, and
the expected result.

**Result legend:** ✅ checked with a script / automated test on 2026-11-11 ·
☐ to check by hand during the final run before the defense.

Useful cheats: `F1` opens the cheat menu (God Mode, No Clip, Freeze Ghosts, Change Level,
Add Lives, Add XP, Add Timer, Time Speed, Give Skills).

## 1. Launch, configuration and robustness

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| C1 | `python3 pac-man.py config.jsonc` / `make run` | The lobby opens | ✅ |
| C2 | Config with `#`, `//` and `/* */` comments, and `#` inside a string | Comments ignored, strings kept | ✅ (pytest) |
| C3 | Missing config file / unreadable file | Warning, game starts with defaults, no traceback | ✅ |
| C4 | `"screen_width": -5` | Warning `Invalid value for screen_width`, falls back to 1280 | ✅ |
| C5 | Unknown key `"foo": 1` | Ignored silently | ✅ |
| C6 | A level with `"level_width": 0`, a level that is a string | Only the bad value is reset, the bad level is skipped, other levels kept | ✅ |
| C7 | `"levels": []` or invalid `levels` | Warning, 10 default levels used | ☐ |
| C8 | Invalid JSON (`{ invalid json }`) | Warning, defaults used | ✅ (pytest) |
| C8b | Config is not a JSON object (`[1, 2]`) | Warning, defaults used | ☐ |
| C9 | `make lint` | flake8 and mypy pass | ✅ |

## 2. Maze generation

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| M1 | Start a run twice | Level 1 is the same maze (seed 42) both times | ✅ |
| M2 | Clear level 1 (cheat *Change Level*) twice in 2 runs | Level 2 is different each run (random seed, printed in logs) | ☐ |
| M3 | Level with an explicit `"seed"` | Same maze at each run | ☐ |
| M4 | Generator fails | Clear `MazeGenerationError` message, no traceback | ✅ |
| M5 | 20×20 maze | The closed "42" cells have no pacgum and cannot be entered | ☐ |

## 3. Gameplay

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| G1 | Move with WASD and arrows | Player moves in corridors only, never in walls | ☐ |
| G2 | Start of a level | Player in the middle, 4 ghosts and 4 super-pacgums in the corners, pacgums everywhere else | ☐ |
| G3 | Eat a pacgum / super-pacgum | Score +3 / +30 (default config); pacgum disappears | ☐ |
| G4 | Eat a super-pacgum | Ghosts turn blue and run away for ~10 s | ☐ |
| G5 | Eat a frightened ghost | Score +60, ghost goes back to its corner as eyes, respawns after ~2 s | ☐ |
| G6 | Touched by a chasing ghost | One life lost, player and ghosts back to their start tiles | ☐ |
| G7 | Lose 3 lives | Game over screen | ☐ |
| G8 | Eat all pacgums | Next level; score and lives kept | ☐ |
| G9 | Finish the last level (cheat *Change Level* ×10) | Victory screen | ☐ |
| G10 | Let the timer reach 0 (cheat *Time Speed*) | Game over | ☐ |
| G11 | Score during the run | Never decreases | ☐ |
| G12 | Ghost personalities (cheat *Wall Hack*) | Blinky targets the player, Pinky 4 tiles ahead, Inky mirror of Blinky, Clyde random border tile | ☐ |
| G13 | Level-up | 3 rings to choose; at most 3 different rings | ☐ |

## 4. User interface

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| U1 | Main menu | Start game, Highscores (Leaderboard), How to play, Settings, Exit | ☐ |
| U2 | HUD during the game | Score, lives, level, remaining time always visible | ☐ |
| U3 | `Esc` in game | Pause menu: resume, or back to the main menu | ☐ |
| U4 | Game over / victory | Final score shown, (congratulations on victory), name asked if top 10 | ☐ |
| U5 | After the end screen | Back to the main menu | ☐ |
| U6 | Settings → rebind a key | New key works, saved after restart | ☐ |
| U7 | Resize the window / fullscreen | Content scaled, mouse clicks at the right place | ☐ |
| U8 | Cheat menu (`F1`) | Every cheat works and only affects the current run | ☐ |

## 5. Highscores

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| H1 | First launch, no file | Empty leaderboard created, no error | ✅ |
| H2 | End a run with an empty leaderboard | Name prompt shown (rank #1) | ✅ (rank 0 computed) / ☐ UI |
| H3 | Name `BOB` | Saved | ✅ |
| H4 | Name with 11 characters / with `_` | Refused (input stops at 10 chars, only letters, digits, spaces) | ✅ |
| H5 | 12 runs saved | Only the top 10 kept, sorted by score | ✅ |
| H6 | Restart the game | Highscores loaded again, best score on the lobby | ✅ |
| H7 | Edit the file by hand / corrupt it | Warning, file ignored, empty leaderboard | ✅ |
| H8 | `highscore_path` set in the config | File created at that path | ✅ |

## 6. Packaging

| ID | Test | Expected | Result |
| --- | --- | --- | :-: |
| P1 | `make build` | `dist/pak-man/` and `dist/pac-man.zip` created | ☐ |
| P2 | Download from itch.io, unzip, launch `pak_man` | Game runs without Python installed | ☐ |

## Bugs found and fixed

From the `fix:` commits (141 in total), the most important ones:

| Date | Bug | Fix |
| --- | --- | --- |
| 2026-09-30 | Moving right went the wrong way | Fixed direction mapping in `Player` |
| 2026-10-05 | Collision bugs | Fixed collision check, re-used `self._colliders` |
| 2026-10-06 | Pacgums inside walls (closed "42" cells) | Skip full tiles when placing pacgums |
| 2026-10-06 | Pacgum not eaten on contact | Fixed collision detection and deletion |
| 2026-10-06 | Wrong direction after death | Reset direction on respawn |
| 2026-10-08 | A\* gave wrong paths | Use a heap, fix `get_possible_moves` wall filter, invalidate the move cache |
| 2026-10-11 | Pinky used its own direction instead of the player's | Use the player's direction |
| 2026-10-12 | Maze seed not applied as expected | Fixed the seed given to the maze generator |
| 2026-10-12 | Inky wrong target, thin walls | Fixed target formula and wall thickness |
| 2026-10-14 / 10-20 | Circular imports | `TYPE_CHECKING`, local imports, `App` container |
| 2026-10-20 | Fonts badly blended, inverted textures | Blending and UV fixes in the renderer |
| 2026-10-23 | Pause menu opened over the level-up menu; player not spawning in the middle | Status checks; spawn formula |
| 2026-10-27 | Lag with many meshes | Optimised `_iter_meshes`, hover |
| 2026-10-28 | Clicks not detected in nested widgets | `Clickable` knows its parents |
| 2026-11-03 | Player moving behind the level-up menu opened by a cheat | Player input ignored while the menu is open |
| 2026-11-09 | Game over screen not quitting; mouse wrong on a resized window | Callbacks; mouse position translation |
| 2026-11-10 | Entities updated in random order | `EntityStore` keeps insertion order |
| 2026-11-11 | Window ghosting when leaving fullscreen | Fixed the fullscreen → windowed switch |
| 2026-11-11 | A run that would be **#1** never asked for a name (rank 0 treated as false) | `if rank is not None` |
| 2026-11-11 | `highscore_path` ignored; names allowed up to 15 chars and any symbol | Use the config path; 10 chars, letters/digits/spaces only |
| 2026-11-11 | One invalid level reset the whole `levels` list; 0×0 maze crashed the generator | Per-level validation, size limits, `MazeGenerationError` |
| 2026-11-11 | Only 3 levels; every level used the same default seed | 10 levels; seed 42 for level 1, random after |
