import multiprocessing
import queue
import threading

from . import consts
from .utils.lifo_queue import LIFOQueue


input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()
notify_queue = multiprocessing.Queue()

frame_queue = LIFOQueue()

task_queue = queue.Queue()
video_queue = queue.Queue(maxsize=10)

CONFIG = None

# 程序运行
G_RUN = threading.Event()

#
G_OUT_WORKER = threading.Event()

# 退出循环事件
G_RACE_RUN_EVENT = threading.Event()
G_RACE_QUIT_EVENT = threading.Event()

# 是否活跃状态
NO_OPERATION_COUNT = 0

# 游戏模式
MODE = ""

# 段位
DIVISION = ""

# 选车次数
SELECT_COUNT = {
    consts.mp1_zh: 0,
    consts.mp2_zh: 0,
    consts.mp3_zh: 0,
    consts.car_hunt_zh: 0,
    consts.legendary_hunt_zh: 0,
    consts.custom_event_zh: 0,
    consts.career_zh: 0,
}
# 是否选车
SELECT_CAR = {
    consts.mp1_zh: True,
    consts.car_hunt_zh: True,
    consts.legendary_hunt_zh: True,
}

# Event
EVENT_UPDATE = False

# 比赛中
RACING = 0

#

SUPPORT_MJPG = None
