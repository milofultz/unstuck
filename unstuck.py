import shutil
from time import sleep

from playsound import playsound


TERMINAL_HEIGHT = shutil.get_terminal_size()[1]

FIVE_MINUTES = 5 * 60
ONE_POMODORO = 25 * 60

RED = "\033[91m"
GREEN = "\033[92m"
WHITE = "\033[97m"
NORMAL = '\033[0m'


def clear_screen():
    print(WHITE + '\n' * TERMINAL_HEIGHT + NORMAL)


def timer(seconds: int, text: str):
    seconds_left = seconds
    while seconds_left > 0:
        try:
            clear_screen()
            print(GREEN + text + NORMAL + WHITE + '\n' + NORMAL)
            print(f'{seconds_left // 3600}:' +
                  f'{((seconds_left // 60) % 60):02}:' +
                  f'{(seconds_left % 60):02} \n')
            print('Press `Ctrl + C` to stop the timer\n')
            sleep(1)
            seconds_left -= 1
        except KeyboardInterrupt:
            break

    if not seconds_left:
        playsound('alert.wav')
    clear_screen()


if __name__ == "__main__":
    blocker = ''
    is_stuck = False
    solutions = list()

    clear_screen()
    while True:
        if is_stuck:
            next_task_num = ''
            while not next_task_num.isdigit():
                print(blocker)
                print(''.join(f'\n{i + 1}. {solution}' for i, solution in enumerate(solutions)))
                next_task_num = input(WHITE + '\nWhich of these solutions could get you closest to success next pomodoro? ' + NORMAL)
                clear_screen()
            next_task = solutions[int(next_task_num) - 1]
        else:
            next_task = input(WHITE + '\nWhat are you working on during the next pomodoro? ' + NORMAL)
        timer(ONE_POMODORO, RED + next_task + NORMAL)
        current_task = input(WHITE + '\nWhat are you working on right now? ' + NORMAL)
        is_stuck = 'y' in input(WHITE + '\nAre you stuck? ' + NORMAL)
        if is_stuck:
            blocker = input(WHITE + '\nExplain what is blocking your progress on this: ' + NORMAL)
            print(WHITE + '\nWhat are the three best or most viable solutions to this problem available to you right now?' + NORMAL)
            del solutions[:]
            solution = input('-> ')
            while solution != '':
                solutions.append(solution)
                solution = input('-> ')
        timer(FIVE_MINUTES, GREEN + 'Take a 5 minute break.' + NORMAL)