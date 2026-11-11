# Project management

This directory documents how **rpetit** (69Nesta) and **lgirard** (B4nJuice) managed the
Pak-Man project, from 8 September to 11 November 2026.

| Document | Content |
| --- | --- |
| [timeline.md](timeline.md) | Gantt chart of the phases, milestones and weekly activity |
| [team_organization.md](team_organization.md) | Who did what, workflow, how decisions were made and issues handled |
| [risk_analysis.md](risk_analysis.md) | Risks found at the start and during the project, and how we reduced them |
| [acceptance_test_plan.md](acceptance_test_plan.md) | Features to test against the subject, bugs found and fixed |
| [blocking_points.md](blocking_points.md) | Main blocking points, conflicts and what we learned |

## Approach in short

1. **Read the subject together** and split it into blocks: engine (rendering, maze,
   entities), gameplay (player, ghosts, items, scoring), UI (menus, HUD), data (config,
   highscores, settings), delivery (packaging, itch.io, documentation).
2. **Design before code**: rpetit made the
   [Figma mockups](https://www.figma.com/design/cSfGNa7qtEZC10juktc8Ys/42---Pakman?node-id=0-1&t=foPbcMUUIEDrhbBq-1)
   of every screen, so we agreed on the look and the flow of the game before building it.
3. **Iterative development**: we first got a playable core (maze + player + ghosts),
   then added features one by one, each in its own branch and pull request.
4. **Continuous quality**: GitHub Actions runs `flake8` and `mypy` on every PR, `pytest`
   covers the config parser, and every change goes through a pull request.
5. **Tracking**: GitHub Issues for bugs and TODOs, GitHub Pull Requests for features,
   in-person and Discord syncs for the planning.

## Key numbers (from git)

| | Value |
| --- | --- |
| Duration | 9 weeks (2026-09-08 → 2026-11-11) |
| Commits (without merges) | 383 — rpetit 163, lgirard 220 |
| Merged pull requests | ~90 (up to PR #148) |
| Commit types | 196 `feat`, 141 `fix`, the rest `refactor` / `chore` / `style` |
| Source files | ~150 Python modules, 9 GLSL shaders |
