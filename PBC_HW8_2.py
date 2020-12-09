from datetime import datetime, timedelta
class Dog:
    def __init__(self, name, height, weight, adopted_date):
        self.name = name
        self.height = height
        self.weight = weight
        self.adopted_date = adopted_date
        self.dust = 0
        self.walk_count = 0
        self.longest_duration = timedelta(0)
        self.last_walk_date = adopted_date
        self.is_small_dog = self.is_small_dog()

    def is_small_dog(self):
        # 判斷是否為小型犬， 回傳boolean 值
        if (self.height > 60) or (self.weight > 30):
            return False
        else:
            return True

    def walk(self , walk_date):
        if self.is_small_dog:
            # 依據小型犬的灰塵累積效率更新累積灰塵量
            self.dust += 3
        else:
            # 依據大型犬的灰塵累積效率更新累積灰塵量
            self.dust += 2
        # 更新散步次數、最大散步間隔時間、最近散步日期
        self.walk_count += 1
        duration = walk_date - self.last_walk_date
        if duration > self.longest_duration:
            self.longest_duration = duration
        self.last_walk_date = walk_date

    def bathe(self):
        # 更新累積灰塵量
        self.dust = 0

    def get_walk_frquency(self, today):
        frquency = self.walk_count / ((today - self.adopted_date).days)
        return frquency

    def __str__(self):
        return ','.join(
            [self.name, str(self.height), str(self.weight), str(self.dust)]
        )

dogs = {}
today_string = input()
today = datetime.strptime(today_string, '%Y/%m/%d')
task = input().split(',')
while True:
    event = input()
    if event == "Done":
        break
    event = event.split('|')
    event_type = event[0]
    name = event[1]

    # 領養
    if event_type == 'A':
        height = int(event[2])
        weight = int(event[3])
        adopted_date = datetime.strptime(event[4], '%Y/%m/%d')
        dogs[name] = Dog(name, height, weight, adopted_date)

    # 散步
    elif event_type == 'W':
        walk_date = datetime.strptime(event[2], '%Y/%m/%d')
        dogs[name].walk(walk_date)

    # 洗澡
    elif event_type == 'B':
        dogs[name].bathe()

    # 換主人
    else:
        goodbye_dog = dogs.pop(name)

task_type = task[0]
if task_type == 'TaskA':
    target_dog_name = task[1]
    target_dog = dogs[target_dog_name]

elif task_type == 'TaskB':
    sorted_dogs = sorted(
        dogs.items(),
        key=lambda dog: [
            dog[1].get_walk_frquency(today),
            dog[1].is_small_dog,
            -dog[1].weight,
            -dog[1].height,
            dog[1].name
        ]
    )
    target_dog = sorted_dogs[0][1]

elif task_type == 'TaskC':
    sorted_dogs = sorted(
        dogs.items(),
        key=lambda dog: [
            -dog[1].longest_duration,
            dog[1].is_small_dog,
            -dog[1].weight,
            -dog[1].height,
            dog[1].name
        ]
    )
    target_dog = sorted_dogs[0][1]

# task D
else:
    sorted_dogs = sorted(
        dogs.items(),
        key=lambda dog: [
            -dog[1].dust,
            dog[1].is_small_dog,
            -dog[1].weight,
            -dog[1].height,
            dog[1].name
        ]
    )
    target_dog = sorted_dogs[0][1]

print(target_dog)
