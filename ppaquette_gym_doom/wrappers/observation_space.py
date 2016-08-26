import gym

try:
    from doom_py import ScreenResolution
except ImportError as e:
    raise gym.error.DependencyNotInstalled("{}. (HINT: you can install Doom dependencies " +
                                           "with 'pip install doom_py.)'".format(e))

resolutions = ['160x120', '200x125', '200x150', '256x144', '256x160', '256x192', '320x180', '320x200',
               '320x240', '320x256', '400x225', '400x250', '400x300', '512x288', '512x320', '512x384',
               '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640',
               '1024x768', '1280x720', '1280x800', '1280x960', '1280x1024', '1400x787', '1400x875',
               '1400x1050', '1600x900', '1600x1000', '1600x1200', '1920x1080']

__all__ = [ 'SetResolution' ]

def SetResolution(target_resolution):

    class SetResolutionWrapper(gym.Wrapper):
        """
            Doom wrapper to change screen resolution
        """
        def __init__(self, env):
            super(SetResolutionWrapper, self).__init__(env)
            if target_resolution not in resolutions:
                raise gym.error.Error('Error - The specified resolution "{}" is not supported by Vizdoom.'.format(target_resolution))
            parts = target_resolution.lower().split('x')
            width = int(parts[0])
            height = int(parts[1])
            screen_res = __import__('doom_py')
            screen_res = getattr(screen_res, 'ScreenResolution')
            screen_res = getattr(screen_res, 'RES_{}X{}'.format(width, height))
            self.screen_width, self.screen_height, self.unwrapped.screen_resolution = width, height, screen_res
            self.unwrapped.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.screen_height, self.screen_width, 3))
            self.observation_space = self.unwrapped.observation_space

    return SetResolutionWrapper
