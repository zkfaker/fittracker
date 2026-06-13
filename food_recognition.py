"""百度AI食物识别模块"""

import base64
import json
import urllib.request
import urllib.parse
from config import BAIDU_API_KEY, BAIDU_SECRET_KEY


def get_access_token():
    """获取百度AI access_token"""
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_API_KEY}&client_secret={BAIDU_SECRET_KEY}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('access_token')
    except Exception as e:
        print(f"获取token失败: {e}")
        return None


def recognize_food(image_path):
    """
    识别食物并返回热量信息
    返回: {"name": "食物名", "calories": 热量, "confidence": 置信度}
    """
    access_token = get_access_token()
    if not access_token:
        return None

    # 读取图片并转base64
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"读取图片失败: {e}")
        return None

    # 调用百度图像识别API（菜品识别）
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v2/dish?access_token={access_token}"

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = urllib.parse.urlencode({
        'image': image_data,
        'top_num': 1,
        'baike_num': 0,
    }).encode('utf-8')

    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))

        if 'result' in result and result['result']:
            dish = result['result'][0]
            name = dish.get('name', '未知食物')
            calorie_str = dish.get('calorie', '0')

            # 解析热量（可能是字符串如"150千卡/100g"）
            try:
                calories = float(''.join(filter(str.isdigit, str(calorie_str).split('千')[0])))
            except:
                calories = 0

            return {
                "name": name,
                "calories": calories,
                "confidence": dish.get('probability', 0),
            }
    except Exception as e:
        print(f"识别失败: {e}")

    return None


def get_food_calories(food_name):
    """
    根据食物名称查询热量（本地数据库）
    返回: 每100克的热量(千卡)
    """
    # 常见食物热量表（每100克）
    food_db = {
        # 主食
        "米饭": 116, "白米饭": 116, "大米饭": 116,
        "面条": 110, "挂面": 110, "拉面": 110,
        "馒头": 221, "花卷": 211, "包子": 227,
        "饺子": 186, "馄饨": 150,
        "油条": 386, "烧饼": 326, "煎饼": 233,
        "面包": 265, "吐司": 265, "全麦面包": 246,
        "粥": 46, "小米粥": 46, "皮蛋瘦肉粥": 58,
        # 肉类
        "猪肉": 143, "五花肉": 395, "里脊肉": 155,
        "牛肉": 125, "牛排": 250, "肥牛": 198,
        "鸡肉": 167, "鸡胸肉": 133, "鸡腿": 181,
        "鸭肉": 240, "鹅肉": 161,
        "羊肉": 203, "排骨": 264,
        # 海鲜
        "鱼": 96, "鲈鱼": 105, "三文鱼": 139,
        "虾": 87, "大虾": 93, "基围虾": 101,
        "螃蟹": 95, "扇贝": 60,
        # 蔬菜
        "白菜": 13, "青菜": 15, "生菜": 13,
        "西兰花": 34, "花菜": 25, "菜花": 25,
        "番茄": 19, "西红柿": 19, "黄瓜": 16,
        "茄子": 25, "土豆": 76, "红薯": 86,
        "胡萝卜": 41, "萝卜": 18, "洋葱": 40,
        "菠菜": 23, "芹菜": 14, "韭菜": 26,
        # 水果
        "苹果": 52, "香蕉": 89, "橙子": 47,
        "葡萄": 69, "草莓": 32, "西瓜": 30,
        "芒果": 60, "桃子": 39, "梨": 52,
        "樱桃": 50, "蓝莓": 57, "猕猴桃": 61,
        # 蛋奶豆
        "鸡蛋": 144, "煎蛋": 196, "蒸蛋": 72,
        "牛奶": 54, "酸奶": 72, "豆浆": 31,
        "豆腐": 76, "豆腐脑": 15, "豆皮": 409,
        # 常见菜品
        "宫保鸡丁": 177, "鱼香肉丝": 180, "麻婆豆腐": 120,
        "红烧肉": 435, "糖醋排骨": 260, "可乐鸡翅": 210,
        "番茄炒蛋": 98, "青椒肉丝": 150, "回锅肉": 250,
        "水煮鱼": 120, "酸菜鱼": 105,
        "炒饭": 180, "蛋炒饭": 190, "扬州炒饭": 200,
        "炒面": 170, "炒河粉": 160,
        # 快餐/零食
        "汉堡": 250, "薯条": 312, "披萨": 266,
        "炸鸡": 280, "薯片": 536, "饼干": 466,
        "巧克力": 546, "蛋糕": 348, "冰淇淋": 207,
        # 饮料
        "可乐": 43, "雪碧": 45, "果汁": 45,
        "奶茶": 65, "咖啡": 2, "绿茶": 1,
        "啤酒": 32, "白酒": 350, "红酒": 85,
    }

    # 模糊匹配
    for key, value in food_db.items():
        if key in food_name or food_name in key:
            return value

    # 未找到，返回默认值
    return 100  # 默认100千卡/100g


if __name__ == "__main__":
    # 测试
    print("测试食物热量查询:")
    print(f"米饭: {get_food_calories('米饭')} kcal/100g")
    print(f"红烧肉: {get_food_calories('红烧肉')} kcal/100g")
    print(f"苹果: {get_food_calories('苹果')} kcal/100g")
