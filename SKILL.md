---
name: bubble-subtitle
description: AR speech bubbles with face tracking and camera vision.
---

# Bubble Subtitle

Call `run_js` with a JSON `data` string. Pick the mode:

## camera (default)
AR speech bubbles over live camera feed.
Trigger: start, go, camera, video, or anything vague.
data: {"mode":"camera","lang":"en-US"}

## snapshot
Capture a photo and return it to you as an image.
Trigger: look, see, take photo, describe, what do you see.
data: {"mode":"snapshot","camera":"user"}

## listen
Record audio, transcribe it, return text to you.
Trigger: listen, hear.
data: {"mode":"listen","seconds":5,"lang":"en-US"}

## record
Audio-only recording with animated bubbles, no camera.
Trigger: record, audio only.
data: {"mode":"record","lang":"en-US"}

## play
Animate a timestamped transcript with bubbles.
Trigger: user provides text with timestamps.
data: {"mode":"play","segments":[{"start":0,"end":3,"text":"Hello","speaker":"A"}]}

Default to camera if intent is unclear. Always call run_js immediately, never ask questions.
