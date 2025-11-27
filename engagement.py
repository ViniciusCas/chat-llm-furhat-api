# engagement.py
from dataclasses import dataclass


@dataclass
class EngagementPolicy:
    inner_radius: float
    outer_radius: float
    max_users: int


# === Engagement policies (mirroring your Kotlin code) ===

def default_engagement_policy() -> EngagementPolicy:
    return EngagementPolicy(
        inner_radius=1.0,
        outer_radius=1.5,
        max_users=2,
    )


def sleeping_engagement_policy() -> EngagementPolicy:
    return EngagementPolicy(
        inner_radius=4.0,
        outer_radius=4.0,
        max_users=2,
    )


def idle_engagement_policy() -> EngagementPolicy:
    return EngagementPolicy(
        inner_radius=2.0,
        outer_radius=4.0,
        max_users=10,
    )


def active_engagement_policy() -> EngagementPolicy:
    return EngagementPolicy(
        inner_radius=1.5,
        outer_radius=2.5,
        max_users=4,
    )


# === Custom locations ===

from dataclasses import dataclass

@dataclass
class Location:
    x: float
    y: float
    z: float


# Equivalent to: val downMax = Location(0.0, -1.0, 3.0)
down_max = Location(0.0, -1.0, 3.0)
