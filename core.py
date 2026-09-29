"""造纸厂核心逻辑：浆料、抄纸机、白水回收和损耗。"""

import json


def new_game():
    return {
        "batches": {},
        "machine_load": 0,
        "machine_capacity": 2,
        "pulp": 100,
        "loss": 0,
        "batch_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    # 读档必须原样恢复，不能让批次跳过一阶段
    return json.loads(text)


def feed(state, batch_id, amount):
    # 同一浆料只能投一次
    if batch_id in state["batches"]:
        return False
    # 抄纸机满负荷时不能再进料
    if state["machine_load"] >= state["machine_capacity"]:
        return False
    state["batches"][batch_id] = amount
    state["machine_load"] += amount
    state["pulp"] -= amount
    return True


def check_moisture(state, moisture):
    # 水分过高（超过上限）才是湿纸，边界方向不能反
    if moisture > 30:
        return "wet"
    return "ok"


def cancel(state, batch_id):
    # 不存在的批次取消无效，重复取消幂等
    if batch_id not in state["batches"]:
        return False
    amount = state["batches"].pop(batch_id)
    state["machine_load"] -= amount
    return True


def produce(state, amount):
    # 白水回收故障时不计产量
    if state.get("whitewater_fault"):
        return False
    return True


def break_event(state):
    # 一次断纸事件只扣一次损耗
    state["loss"] += 10
    return state["loss"]


def start(state):
    # 浆料不足不能开机
    if state.get("pulp", 0) <= 0:
        return False
    return True


def main():
    print("造纸厂 - 命令: feed/moisture/cancel/produce/break/start/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd = parts[0]
        result = None
        try:
            if cmd == "feed":
                result = feed(state, int(parts[1]), int(parts[2]))
            elif cmd == "moisture":
                result = check_moisture(state, int(parts[1]))
            elif cmd == "cancel":
                result = cancel(state, int(parts[1]))
            elif cmd == "produce":
                result = produce(state, int(parts[1]))
            elif cmd == "break":
                result = break_event(state)
            elif cmd == "start":
                result = start(state)
        except (IndexError, ValueError):
            result = None
        if result is True:
            print("ok")
        elif result is False:
            print("fail")
        else:
            print(result)


if __name__ == "__main__":
    main()
