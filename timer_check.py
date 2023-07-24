from resettabletimer import ResettableTimer
import time


def timer_fn():
    print(time.time())


def main():
    print(time.time())
    timer = ResettableTimer(5, timer_fn)
    timer.start()
    time.sleep(2)
    timer.reset()
    time.sleep(10)


if __name__ == '__main__':
    main()
