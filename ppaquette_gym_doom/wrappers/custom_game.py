import os
import types
import gym

try:
    import doom_py
    from doom_py import DoomGame, Mode, Button, GameVariable, ScreenFormat, ScreenResolution, Loader
except ImportError as e:
    raise gym.error.DependencyNotInstalled("{}. (HINT: you can install Doom dependencies " +
                                           "with 'pip install doom_py.)'".format(e))

__all__ = [ 'CustomGame' ]

def CustomGame():

    def _customize_game(self):
        vizdoom_path = self.loader.get_vizdoom_path()   # paths are based on installation path of doom_py
        freedoom_path = self.loader.get_freedoom_path()
        doom_dir = self.doom_dir                        # dirname of directory containing 'doom_env'

        # Settings
        config = os.path.join(doom_dir, 'assets', 'deadly_corridor.cfg')
        scenario = self.loader.get_scenario_path('deadly_corridor.wad')
        map = ''
        difficulty = 1

        # Customizing - self.game refers to a new DoomGame()
        self.game.set_vizdoom_path(vizdoom_path)
        self.game.set_doom_game_path(freedoom_path)
        self.game.load_config(config)
        self.game.set_doom_scenario_path(scenario)
        if map != '':
            self.game.set_doom_map(map)
        self.game.set_doom_skill(difficulty)
        self.game.set_screen_resolution(self.screen_resolution)

    class CustomGameWrapper(gym.Wrapper):
        """
            Doom wrapper to load a custom map
            This wrapper modifies directly the unwrapped env, and is not expected to be stacked
        """
        def __init__(self, env):
            super(CustomGameWrapper, self).__init__(env)
            self.unwrapped.action_space = gym.spaces.MultiDiscrete([[0, 1]] * 38 + [[-10, 10]] * 2 + [[-100, 100]] * 3)   # Default 43 button action space
            self.unwrapped.screen_height = 480
            self.unwrapped.screen_width = 640
            self.unwrapped.screen_resolution = ScreenResolution.RES_640X480
            self.unwrapped.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.unwrapped.screen_height, self.unwrapped.screen_width, 3))
            self.observation_space = self.unwrapped.observation_space
            self.unwrapped.allowed_actions = [0, 10, 11, 13, 14, 15]        # Must match exactly and in order the actions in the config file
                                                                            # (The number is the action number based on controls.md)
                                                                            # This will only enable these actions out of the 43 available buttons

            # Converting to Discrete action space
            discrete_actions = self.unwrapped.allowed_actions
            self.action_space = gym.spaces.DiscreteToMultiDiscrete(self.unwrapped.action_space, discrete_actions)

            # Alternative to convert to continuous action space
            # box_actions = self.unwrapped.allowed_actions
            # self.action_space = gym.spaces.BoxToMultiDiscrete(self.unwrapped.action_space, box_actions)

            # Bouding method to env
            self.unwrapped._customize_game = types.MethodType(_customize_game, self.unwrapped)

        def _step(self, action):
            return self.unwrapped._step(self.action_space(action))

    return CustomGameWrapper
