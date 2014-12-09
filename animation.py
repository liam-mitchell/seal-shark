import pygame

class Animation(object):
    def __init__(self, frames, frame_duration):
        self.current_time = 0
        self.frame_number = 0
        self.frames = []
        for f in frames:
            self.frames.append(f)
        self.frame_duration = frame_duration

    def current_frame(self):
        return self.frames[self.frame_number]

    def next_frame(self, dt):
        if self.frame_duration == 0:
            return self.frames[0]

        self.current_time += dt
        if self.current_time > self.frame_duration:
            self.frame_number += 1
            self.current_time = 0
            if self.frame_number == len(self.frames):
                self.frame_number = 0

        return self.frames[self.frame_number]


class PlayOnceAnimation(Animation):
    def __init__(self, frames, frame_duration):
        Animation.__init__(self, frames, frame_duration)

    def next_frame(self, dt):
        if self.frame_number == len(self.frames) - 1:
            self.frame_duration = 0

        if self.frame_duration == 0:
            return self.frames[len(self.frames) - 1]

        self.current_time += dt
        if self.current_time > self.frame_duration:
            self.frame_number += 1
            self.current_time = 0
            if self.frame_number == len(self.frames):
                self.frame_number = 0

        return self.frames[self.frame_number]
