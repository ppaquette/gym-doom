# gym-doom
#### **Gym Doom is an environment bundle for OpenAI Gym**
---
<div id="installation"></div>Installation
============

You need to install [gym-pull](https://github.com/ppaquette/gym-pull)

```shell
    pip install gym-pull
```

 To load and run the environments, run

```python
    import gym
	import gym_pull
	gym_pull.pull('github.com/ppaquette/gym-doom')        # Only required once, envs will be loaded with import gym_pull afterwards
	env = gym.make('ppaquette/DoomBasic-v0')
```

Environments included:
============
- ppaquette/meta-Doom-v0
- ppaquette/DoomBasic-v0
- ppaquette/DoomCorridor-v0
- ppaquette/DoomDefendCenter-v0
- ppaquette/DoomDefendLine-v0
- ppaquette/DoomHealthGathering-v0
- ppaquette/DoomMyWayHome-v0
- ppaquette/DoomPredictPosition-v0
- ppaquette/DoomTakeCover-v0
- ppaquette/DoomDeathmatch-v0
