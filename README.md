# PushPwn

PushPwn is a MIDI controller–based tactile security operations platform that orchestrates autonomous reconnaissance agents with real-time visual feedback.

## Overview

PushPwn transforms MIDI hardware (such as Ableton Push) into a physical control surface for launching and monitoring parallel security agents.

Each pad represents an independent agent that:
- Starts/stops with a press
- Runs continuous monitoring tasks
- Provides real-time visual feedback via LED states

## Features

- 🎛️ MIDI controller integration (Ableton Push, etc.)
- 🧠 Agent-based architecture
- 🔁 Parallel execution (threaded agents)
- 🚨 Real-time alert feedback
- 🎨 LED state visualization

## Demo Behavior

| State  | Color  |
|--------|--------|
| Idle   | Off    |
| Active | White  |
| Alert  | Red    |

## Installation

```bash
pip install -r requirements.txt
