# Timeline

The dates below are the **actual** dates, rebuilt from the git history (first and last
commit of each block of work).

## Gantt chart

```mermaid
gantt
    title Pak-Man — actual timeline
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section Setup & design
    Repo, uv, Makefile, gitignore          :done, s1, 2026-09-08, 2d
    Config model + comment parser          :done, s3, 2026-09-09, 8d
    Logger, lint, mypy                     :done, s4, 2026-09-15, 2d

    section Engine
    CPU drawing prototype                  :done, e1, 2026-09-08, 2d
    GPU renderer (moderngl, shaders)       :done, e2, 2026-09-10, 13d
    Maze adapter (mazegenerator) + Level   :done, e3, 2026-09-08, 16d
    Meshes, SuperMeshes, text & fonts      :done, e4, 2026-09-19, 6d
    Entities, movement, Displayable        :done, e5, 2026-09-21, 10d

    section Gameplay
    Player, pacgums, collisions, lives     :done, g1, 2026-09-30, 7d
    Ghost AI, A*, Blinky / Pinky           :done, g2, 2026-10-05, 5d
    Inky / Clyde, ghost states, frightened :done, g3, 2026-10-11, 3d
    Rings (ameliorations) & skills         :done, g4, 2026-10-14, 8d
    Timer, levels, next level              :done, g5, 2026-10-09, 28d

    section Assets
    Texture packs, animations              :done, a1, 2026-10-14, 7d
    Fonts in texture pack                  :done, a2, 2026-10-20, 7d

    section UI
    HUD, stats, pause menu                 :done, u1, 2026-09-29, 30d
    Level-up / ring cards, skills panel    :done, u2, 2026-10-16, 12d
    Buttons, hover, click, key manager     :done, u3, 2026-10-23, 7d
    Cheat menu                             :done, u4, 2026-11-02, 2d
    Lobby, victory, game over, how to play :done, u5, 2026-11-02, 3d
    Leaderboard, settings, save run        :done, u6, 2026-11-04, 7d
    Interface manager, connect all screens :done, u7, 2026-11-04, 6d

    section Data
    Leaderboard core (signed)              :done, d1, 2026-10-22, 5d
    Settings & key bindings                :done, d2, 2026-10-23, 4d

    section Quality & delivery
    CI (flake8 + mypy)                     :done, q1, 2026-10-20, 2d
    Norm / mypy clean-up                   :done, q2, 2026-10-21, 1d
    PyInstaller build, CLI config          :done, q3, 2026-11-09, 1d
    Resizable window, fullscreen           :done, q4, 2026-11-09, 3d
    Docstrings, README, PM docs            :done, q5, 2026-11-11, 1d
```

## Milestones

| Date | Milestone |
| --- | --- |
| 2026-09-08 | Project created, assigned maze package integrated |
| 2026-09-15 | Config system done (comments, fallback to defaults, no traceback) |
| 2026-09-23 | First maze displayed on screen with the GPU renderer |
| 2026-09-30 | Player and entities moving in the maze |
| 2026-10-08 | **First playable version**: eat pacgums, lose lives, eat ghosts in super mode |
| 2026-10-11 | 4 ghosts with their own AI |
| 2026-10-21 | Texture packs, CI green (flake8 + mypy) |
| 2026-10-26 | Leaderboard and settings cores |
| 2026-11-04 | All menus built (lobby, victory, game over, how to play, leaderboard) |
| 2026-11-09 | **Full game loop connected**, first packaged build |
| 2026-11-11 | Docstrings, README and project-management documents |

## Weekly activity (commits, merges excluded)

| Week | Dates | rpetit | lgirard | Main focus |
| --- | --- | ---: | ---: | --- |
| W37 | 08/09 – 14/09 | 4 | 11 | Setup, drawing prototype, maze package |
| W38 | 15/09 – 21/09 | 9 | 5 | Config, logger, GPU renderer, image mesh |
| W39 | 22/09 – 28/09 | 10 | 13 | Maze display, text, Displayable, MeshLayer |
| W40 | 29/09 – 05/10 | 11 | 17 | Entities, player, HUD, pause, first ghost |
| W41 | 06/10 – 12/10 | 29 | 40 | A\*, ghost AI, collisions, lives, super mode, timer |
| W42 | 13/10 – 19/10 | 15 | 22 | Ghost states, rings, texture packs, animations |
| W43 | 20/10 – 26/10 | 29 | 47 | CI, mypy, leaderboard, settings, buttons, level-up UI |
| W44 | 27/10 – 02/11 | 10 | 28 | Hover / click, optimisation, cheat menu |
| W45 | 03/11 – 09/11 | 29 | 18 | All menus, interface manager, levels, build |
| W46 | 10/11 – 11/11 | 17 | 19 | Fixes, fullscreen, docstrings, documentation |

```mermaid
xychart-beta
    title "Commits per week"
    x-axis [W37, W38, W39, W40, W41, W42, W43, W44, W45, W46]
    y-axis "Commits" 0 --> 80
    bar [15, 14, 23, 28, 69, 37, 76, 38, 47, 36]
```

## Progress analysis

- **Weeks 1–4**: most of the time went into the **rendering engine**. Writing our own GPU
  renderer was slower than using a game library, but it was needed to respect the
  "MLX-like functions only" rule and it made every later UI screen easier.
- **Week 5 (W41)** was the turning point: the game became playable, and the ghost AI was
  done in a few days thanks to the `Maze` / `AI` / `A*` base built before.
- **Weeks 6–8**: we added our own **ring progression** system; this was extra work beyond
  the subject, which pushed the menus to the end of the project.
- **Weeks 8–9**: menus were built quickly from the Figma mockups and the shared `Button`
  widgets; the last days were used for connecting every screen, packaging and documentation.
- What we would do differently: build a minimal version of all menus earlier, to test the
  full game loop (menu → game → highscore → menu) sooner.
