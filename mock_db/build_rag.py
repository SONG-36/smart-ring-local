# mock_db/build_rag.py
import chromadb

def build_expert_knowledge_base():
    print("🛠️ 正在启动本地 Chroma 向量数据库引擎...")
    
    # 1. 物理寻址：在本地硬盘新建一个名为 rag_data 的文件夹存放向量数据
    client = chromadb.PersistentClient(path="./rag_data")
    
    # 2. 创建一个名为 "sleep_medicine_papers" 的集合 (Collection)
    # 如果已经存在，就直接获取它
    collection = client.get_or_create_collection(name="sleep_medicine_papers")
    
    print("📚 正在将《顶级睡眠医学论文》进行 Embedding 向量化并落盘...")
    
    # 3. 核心知识灌入：这是你未来的产品护城河
    papers = [
        "《柳叶刀睡眠医学 2024》: 当用户的 HRV（心率变异性）低于 30ms 时，表明其中枢神经系统处于极度疲劳或高压状态。干预建议：睡前 2 小时严禁摄入咖啡因，并进行 15 分钟的 4-7-8 深度呼吸法，可有效提升次日 HRV。",
        "《斯坦福可穿戴设备白皮书》: 夜间频繁的体动（Restless Movements 大于 10 次）通常与睡眠呼吸暂停或卧室温度过高有关。将卧室温度调节至 18.3°C (65°F) 是减少夜间翻身的最有效物理干预手段。",
        "《哈佛健康指南》: 完美的静息心率 (Resting Heart Rate) 在深度睡眠期间应逼近 50-60 bpm。如果用户的夜间心率异常升高，通常是睡前饮酒或高强度深夜运动导致的延迟性代谢反应。"
    ]
    
    # 4. 执行写入：Chroma 会自动在后台调用极速的本地 Embedding 模型，把文字变成数学向量
    collection.add(
        documents=papers,
        metadatas=[{"source": "Lancet"}, {"source": "Stanford"}, {"source": "Harvard"}],
        ids=["paper_1", "paper_2", "paper_3"]
    )
    
    print("✅ 专家知识库构建完成！向量数据已永久保存在 ./rag_data 目录下。")

if __name__ == "__main__":
    build_expert_knowledge_base()