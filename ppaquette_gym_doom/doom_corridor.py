import logging
from .doom_env import DoomEnv

logger = logging.getLogger(__name__)


class DoomCorridorEnv(DoomEnv):
    """
    ------------ Training Mission 2 - Corridor ------------
    This map is designed to improve your navigation. There is a vest
    at the end of the corridor, with 6 enemies (3 groups of 2). Your goal
    is to get to the vest as soon as possible, without being killed.

    Allowed actions:
        [0]  - ATTACK                           - Shoot weapon - Values 0 or 1
        [10] - MOVE_RIGHT                       - Move to the right - Values 0 or 1
        [11] - MOVE_LEFT                        - Move to the left - Values 0 or 1
        [13] - MOVE_FORWARD                     - Move forward - Values 0 or 1
        [14] - TURN_RIGHT                       - Turn right - Values 0 or 1
        [15] - TURN_LEFT                        - Turn left - Values 0 or 1
    Note: see controls.md for details

    Rewards:
        + dX    - For getting closer to the vest
        - dX    - For getting further from the vest
        -100    - Penalty for being killed

    Goal: 1,000 points
        Reach the vest (or at least get past the guards in the 3rd group)

    Ends when:
        - Player touches vest
        - Player is dead
        - Timeout (1 minutes - 2,100 frames)

    Actions:
        actions = [0] * 43
        actions[0] = 0       # ATTACK
        actions[10] = 1      # MOVE_RIGHT
        actions[11] = 0      # MOVE_LEFT
        actions[13] = 0      # MOVE_FORWARD
        actions[14] = 0      # TURN_RIGHT
        actions[15] = 0      # TURN_LEFT

    Configuration:
        After creating the env, you can call env.configure() to configure some parameters.

        - lock [e.g. env.configure(lock=multiprocessing_lock)]

            VizDoom requires a multiprocessing lock when running across multiple processes, otherwise the vizdoom instance
            might crash on launch

            You can either:

            1) [Preferred] Create a multiprocessing.Lock() and pass it as a parameter to the configure() method
                [e.g. env.configure(lock=multiprocessing_lock)]

            2) Create and close a Doom environment before running your multiprocessing routine, this will create
                a singleton lock that will be cached in memory, and be used by all Doom environments afterwards
                [e.g. env = gym.make('Doom-...'); env.close()]

            3) Manually wrap calls to reset() and close() in a multiprocessing.Lock()

    Wrappers:

        You can use wrappers to further customize the environment. Wrappers need to be manually copied from the wrappers folder.

            theWrapperOne = WrapperOneName(init_options)
            theWrapperTwo = WrapperTwoName(init_options)
            env = gym.make('ppaquette/DoomCorridor-v0')
            env = theWrapperTwo(theWrapperOne((env))

        - Observation space:

            You can change the resolution by using the SetResolution wrapper.

                wrapper = SetResolution(target_resolution)
                env = wrapper(env)

            The following are valid target_resolution that can be used:

                '160x120', '200x125', '200x150', '256x144', '256x160', '256x192', '320x180', '320x200',
                '320x240', '320x256', '400x225', '400x250', '400x300', '512x288', '512x320', '512x384',
                '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640',
                '1024x768', '1280x720', '1280x800', '1280x960', '1280x1024', '1400x787', '1400x875',
                '1400x1050', '1600x900', '1600x1000', '1600x1200', '1920x1080'

        - Action space:

            You can change the action space by using the ToDiscrete or ToBox wrapper

                wrapper = ToBox(config_options)
                env = wrapper(env)

            The following are valid config options (for both ToDiscrete and ToBox)

                - minimal       - Only the level's allowed actions (and NOOP for discrete)
                - constant-7    - 7 minimum actions required to complete all levels (and NOOP for discrete)
                - constant-17   - 17 most common actions required to complete all levels (and NOOP for discrete)
                - full          - All available actions (and NOOP for discrete)

            Note: Discrete action spaces only allow one action at a time, Box action spaces support simultaneous actions

        - Control:

            You can play the game manually with the SetPlayingMode wrapper.

                wrapper = SetPlayingMode('human')
                env = wrapper(env)

            Valid options are 'human' or 'algo' (default)

    -----------------------------------------------------
    """
    def __init__(self):
        super(DoomCorridorEnv, self).__init__(1)
