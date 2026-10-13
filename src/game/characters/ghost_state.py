from enum import Enum


class GhostState(Enum):
    CHASE = 'chase'
    FRIGHTENED = 'frightened'
    EATEN = 'eaten'
    WAITING_RESPAWN = 'waiting_respawn'
