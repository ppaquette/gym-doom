"""
------------        Meta - Doom         ------------
This is a meta map that combines all 9 Doom levels.

Levels:

    0   - Doom Basic
    1   - Doom Corridor
    2   - Doom DefendCenter
    3   - Doom DefendLine
    4   - Doom HealthGathering
    5   - Doom MyWayHome
    6   - Doom PredictPosition
    7   - Doom TakeCover
    8   - Doom Deathmatch

Goal: 9,000 points
    - Pass all levels

Scoring:
    - Each level score has been standardized on a scale of 0 to 1,000
    - The passing score for a level is 990 (99th percentile)
    - A bonus of 450 (50 * 9 levels) is given if all levels are passed
    - The score for a level is the average of the last 3 tries
    - If there has been less than 3 tries for a level, the missing tries will have a score of 0
      (e.g. if you score 1,000 on the first level on your first try, your level score will be (1,000+0+0)/ 3 = 333.33)
    - The total score is the sum of the level scores, plus the bonus if you passed all levels.

    e.g. List of tries:

    - Level 0: 500
    - Level 0: 750
    - Level 0: 800
    - Level 0: 1,000
    - Level 1: 100
    - Level 1: 200

    Level score for level 0 = [1,000 + 800 + 750] / 3 = 850     (Average of last 3 tries)
    Level score for level 1 = [200 + 100 + 0] / 3 = 100         (Tries not completed have a score of 0)
    Level score for levels 2 to 8 = 0
    Bonus score for passing all levels = 0
    ------------------------
    Total score = 850 + 100 + 0 + 0 = 950

Changing Level:
    - To unlock the next level, you must achieve a level score (avg of last 3 tries) of at least 600
      (i.e. passing 60% of the last level)
    - There are 2 ways to change level:

    1) Manual method

        - obs, reward, is_finished, info = env.step(action)
        - if is_finished is true, you can call env.change_level(level_number) to change to an unlocked level
        - you can see
            the current level with info["LEVEL"]
            the list of level score with info["SCORES"],
            the list of locked levels with info["LOCKED_LEVELS"]
            your total score with info["TOTAL_REWARD"]

        e.g.
            import gym
            env = gym.make('meta-Doom-v0')
            env.reset()
            total_score = 0
            while total_score < 9000:
                action = [0] * 43
                obs, reward, is_finished, info = env.step(action)
                env.render()
                total_score = info["TOTAL_REWARD"]
                if is_finished:
                    env.change_level(level_you_want)

    2) Automatic change

        - if you don't call change_level() and the level is finished, the system will automatically select the
          unlocked level with the lowest level score (which is likely to be the last unlocked level)

        e.g.
            import gym
            env = gym.make('meta-Doom-v0')
            env.reset()
            total_score = 0
            while total_score < 9000:
                action = [0] * 43
                obs, reward, is_finished, info = env.step(action)
                env.render()
                total_score = info["TOTAL_REWARD"]

Allowed actions:
    - Each level has their own allowed actions, see each level for details

Actions:
    actions = [0] * 43
    actions[0] = 0       # ATTACK
    actions[1] = 0       # USE
    [...]
    actions[42] = 0      # MOVE_UP_DOWN_DELTA
    A full list of possible actions is available in controls.md

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
        env = gym.make('ppaquette/meta-Doom-v0')
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