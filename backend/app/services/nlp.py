import re
from collections import Counter
import jieba


STOPWORDS = {
    "的", "了", "是", "在", "和", "也", "就", "都", "而", "及", "與", "或",
    "一個", "我們", "你", "我", "他", "她", "它", "可以", "如果", "因為",
    "使用", "提供", "更多", "相關", "目前", "以及", "這個", "這些", "自己",
    "不是", "沒有", "但是", "就是", "可能", "需要", "看到", "進行",
    "文章", "內容", "網站", "新聞", "分享", "留言", "登入", "註冊"
}


def extract_entities(text: str, top_k: int = 30):
    """
    Extract simple Chinese entities / keywords from article text.

    This version uses jieba word segmentation and frequency counting.
    """

    if not text:
        return {
            "entity_total_count": 0,
            "unique_entity_count": 0,
            "entities": []
        }

    # Remove URLs, emails, and symbols
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", " ", text)

    words = jieba.lcut(text)

    candidates = []

    for word in words:
        word = word.strip()

        if not word:
            continue

        # Remove very short words, but keep terms like 4G, 5G
        if len(word) < 2 and not re.match(r"^[0-9]+G$", word, re.I):
            continue

        if word in STOPWORDS:
            continue

        # Remove pure numbers
        if word.isdigit():
            continue

        candidates.append(word)

    counter = Counter(candidates)

    entities = [
        {
            "entity": entity,
            "count": count
        }
        for entity, count in counter.most_common(top_k)
    ]

    return {
        "entity_total_count": sum(counter.values()),
        "unique_entity_count": len(counter),
        "entities": entities
    }
    
def classify_entity_topic(entity: str) -> str:
    """
    Classify an entity into a topic group by simple rule-based keywords.
    """

    telecom_keywords = [
        "中華電信", "中華", "遠傳", "台灣大哥大", "台灣大", "台哥大",
        "亞太", "台灣之星", "電信", "電信商", "門號"
    ]

    plan_keywords = [
        "4G", "5G", "吃到飽", "上網", "流量", "網速", "行動上網",
        "熱點", "分享", "網路", "傳輸", "下載", "速度"
    ]

    price_keywords = [
        "月租", "資費", "費率", "價格", "方案", "優惠", "折扣",
        "599", "699", "799", "999", "1399", "費用", "元"
    ]

    contract_keywords = [
        "合約", "綁約", "續約", "攜碼", "新申辦", "限速",
        "違約金", "學生", "老客戶", "申辦", "限制"
    ]

    device_keywords = [
        "手機", "iPhone", "Android", "SIM", "eSIM", "平板",
        "分享器", "設備", "裝置"
    ]

    for keyword in telecom_keywords:
        if keyword.lower() in entity.lower():
            return "電信品牌"

    for keyword in plan_keywords:
        if keyword.lower() in entity.lower():
            return "網路方案"

    for keyword in price_keywords:
        if keyword.lower() in entity.lower():
            return "價格費率"

    for keyword in contract_keywords:
        if keyword.lower() in entity.lower():
            return "合約限制"

    for keyword in device_keywords:
        if keyword.lower() in entity.lower():
            return "設備裝置"

    return "其他"


def group_entities_by_topic(analyzed_results: list):
    """
    Group entities from all analyzed articles into topic clusters.

    Args:
        analyzed_results: results from /api/analyze

    Returns:
        Topic-level entity statistics.
    """

    topic_groups = {}

    for article in analyzed_results:
        entities = article.get("entities", [])

        for item in entities:
            entity = item.get("entity", "")
            count = item.get("count", 0)

            if not entity:
                continue

            topic = classify_entity_topic(entity)

            if topic not in topic_groups:
                topic_groups[topic] = {
                    "topic": topic,
                    "total_count": 0,
                    "unique_entity_count": 0,
                    "entities": {}
                }

            topic_groups[topic]["total_count"] += count

            if entity not in topic_groups[topic]["entities"]:
                topic_groups[topic]["entities"][entity] = 0

            topic_groups[topic]["entities"][entity] += count

    output = []

    for topic, data in topic_groups.items():
        entity_list = [
            {
                "entity": entity,
                "count": count
            }
            for entity, count in sorted(
                data["entities"].items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]

        output.append({
            "topic": topic,
            "total_count": data["total_count"],
            "unique_entity_count": len(entity_list),
            "entities": entity_list[:30]
        })

    output = sorted(output, key=lambda x: x["total_count"], reverse=True)

    return output