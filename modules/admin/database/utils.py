from core.config import users_table, mining_table


def change_value(name: str, value: float) -> None:
    match name:
        case "start_reward":
            users_table.start_reward = value
        case "referal_reward":
            users_table.referal_reward = value
        case "global_booster":
            mining_table.global_booster = value
        case "upgrade_discount":
            mining_table.upgrade_discount = value
    return None


def get_value(content: list) -> any:
    table: str = content[0]
    param: str = content[1]
    filter_name: str = content[2]
    filter_value: any = content[3]
    filter_value_type: str = content[4]

    match filter_value_type:
        case "str":
            filter_value = str(filter_value)
        case "int":
            filter_value = int(filter_value)
        case "float":
            filter_value = float(filter_value)

    response = None
    match table:
        case "users":
            response: any = users_table.get_value(param, filter_name, filter_value)
        case "mining":
            response: any = mining_table.get_value(param, filter_name, filter_value)
    return response
