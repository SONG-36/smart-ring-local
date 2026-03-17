# services/ai_generator/handler.py
import os
import chromadb
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from mock_db.database import SessionLocal, SleepRecord

# Load environment variables
load_dotenv()

# ==========================================
# 1. Tool Definition (The Agent's hands)
# ==========================================

@tool
def get_user_sleep_data(user_id: str) -> str:
    """
    ALWAYS use this tool FIRST to get the user's real-time physical metrics from the database.
    """
    print(f"\n[🧠 AI 大脑神经元触发] 大模型正在索要 {user_id} 的真实物理数据...")
    
    db = SessionLocal()
    try:
        record = db.query(SleepRecord).filter(SleepRecord.user_id == user_id).order_by(SleepRecord.id.desc()).first()
        
        if not record:
            print(f"[❌ AI 探针] 数据库中未找到 {user_id} 的数据。")
            return f"No sleep data found for user {user_id}. Tell the user to sync their ring first."
        
        prompt_data = (
            f"Here is the real-time telemetry data for {user_id}:\n"
            f"- Health Score: {record.sleep_score}/100\n"
            f"- Heart Rate: {record.heart_rate} bpm\n"
            f"- HRV: {record.hrv} ms\n"
            f"- Restless Movements: {record.movement} times\n"
        )
        print(f"[✅ AI 探针] 成功从 SQLite 提取真实数据，已打包成 Prompt 喂给大模型！\n")
        return prompt_data
    except Exception as e:
        print(f"[🔥 AI 探针崩溃] 数据库查询失败: {e}")
        return f"System error while accessing the database: {str(e)}"
    finally:
        db.close()

# 【双持武器改造 1】：极其重要！必须加上 @tool 装饰器！
@tool
def search_medical_literature(symptom_query: str) -> str:
    """
    ALWAYS use this tool SECOND. 
    Use this to search the authoritative medical database for scientific explanations of abnormal metrics.
    Input should be a specific metric or symptom, e.g., "HRV 65" or "Restless movements 10 times".
    """
    print(f"\n[📖 RAG 引擎触发] 大模型正在浩瀚的医学文献中检索: '{symptom_query}'...")
    
    try:
        client = chromadb.PersistentClient(path="./rag_data")
        collection = client.get_collection(name="sleep_medicine_papers")
        
        results = collection.query(
            query_texts=[symptom_query],
            n_results=1 
        )
        
        if results['documents'] and results['documents'][0]:
            matched_paper = results['documents'][0][0]
            print(f"[✅ RAG 命中] 找到高度相关的权威文献！")
            return f"Medical Knowledge Reference: {matched_paper}"
        else:
            return "No relevant medical literature found."
    except Exception as e:
        print(f"[🔥 RAG 引擎崩溃] {e}")
        return "Expert database temporarily offline."

# ==========================================
# 2. LLM Initialization & Agent Assembly
# ==========================================
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

# 【双持武器改造 2】：把 RAG 钳子交给大模型！
tools = [get_user_sleep_data, search_medical_literature]

agent_executor = create_react_agent(llm, tools)

# 【双持武器改造 3】：最高系统指令，逼迫它使用 RAG！
system_prompt = (
    "You are an elite wearable device health coach. "
    "You have access to TWO tools:\n"
    "1. get_user_sleep_data: ALWAYS use this first to get the user's real-time metrics.\n"
    "2. search_medical_literature: ALWAYS use this second. Take the exact metrics from the first tool "
    "and search the medical database for scientific explanations.\n\n"
    "CRITICAL RULE: NEVER give generic advice. Your final advice MUST explicitly quote the "
    "'Medical Knowledge Reference' you found using the second tool."
)

# ==========================================
# 3. API Gateway Entry Point
# ==========================================
def invoke_sleep_coach(user_id: str, query: str) -> str:
    """
    Entry point for the FastAPI router.
    """
    contextual_query = f"User ID is '{user_id}'. The user asks: {query}"
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=contextual_query)
        ]
        
        result = agent_executor.invoke({"messages": messages})
        final_message = result["messages"][-1].content
        return final_message
    except Exception as e:
        print(f"[LangGraph Error] {str(e)}")
        return "System Error: AI Coach is currently unavailable."