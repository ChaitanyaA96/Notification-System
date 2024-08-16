from enum import Enum


class Event:
    def __init__(self, event_type, initiated_by, initiated_at, target_group=-1):
        self.event_type = event_type
        self.initiated_by = initiated_by
        self.initiated_at = initiated_at
        self.target_group = target_group

    def __str__(self):
        return f"{self.event_type} {self.initiated_by} {self.initiated_at} {self.event_type} {self.target_group}"


class EventType(str, Enum):
    Post = "post"
    Follow = "follow"
    Unfollow = "unfollow"
    Live_video = "live_video"
    Like = "like"
    Comment = "comment"