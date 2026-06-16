import random
import time


class RandomWait:
    def __init__(self):
        self.action_count = 0
        self.next_short_break = random.randint(35, 70)
        self.next_long_break = random.randint(350, 700)

    def wait(self):
        self.action_count += 1

        # 长休息优先
        if self.action_count >= self.next_long_break:
            sleep_time = random.randint(5 * 60, 15 * 60)

            print(
                f"[{self.action_count}] 长休息 "
                f"{sleep_time // 60}分{sleep_time % 60}秒"
            )

            time.sleep(sleep_time)

            self.next_long_break += random.randint(350, 700)

        # 短休息
        elif self.action_count >= self.next_short_break:
            sleep_time = random.randint(60, 5 * 60)

            print(
                f"[{self.action_count}] 短休息 "
                f"{sleep_time // 60}分{sleep_time % 60}秒"
            )

            time.sleep(sleep_time)

            self.next_short_break += random.randint(35, 70)

        # 普通间隔
        else:
            sleep_time = random.uniform(1, 5)

            print(
                f"[{self.action_count}] 普通等待 "
                f"{sleep_time:.2f}秒"
            )

            time.sleep(sleep_time)