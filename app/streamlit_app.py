import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, "src"))

import streamlit as st
from agents.tool_selector import tool_selector
from memory.memory_manager import MemoryManager
import os
from dotenv import load_dotenv

# 🔧 Add src/ to path so we can import agents and memory
sys.path.append(os.path.abspath("src"))

from agents.tool_selector import tool_selector
from memory.memory_manager import MemoryManager

load_dotenv()
memory = MemoryManager()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


# 1. Load environment variables and memory
load_dotenv()
memory = MemoryManager()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 2. Streamlit UI
st.title("🧠 GenAI Research Agent")

# Query input
query = st.text_input("Enter your research query:")

# Tool selection
tool_option = st.selectbox("Choose a tool", ["wiki", "web", "pdf"])
use_memory = st.checkbox("Use FAISS memory", value=True)

# PDF upload (if applicable)
uploaded_file = st.file_uploader("Upload a PDF (for PDF tool only)", type=["pdf"])
pdf_path = None
if uploaded_file:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())
    pdf_path = "temp_uploaded.pdf"

# Run
if st.button("Run Agent"):
    context = memory.search_memory(query) if use_memory else []

    if len(context) >= 1:
        st.markdown("### 🧠 Found in memory:")
        unique_context = list(set(context))  # ✅ remove duplicates
        for i, mem in enumerate(unique_context):
            st.markdown(f"**{i+1}.** {mem}")

    else:
        # Use selected tool
        result = tool_selector(query, context_type=tool_option, file_path=pdf_path,
                               api_keys={"SERPER_API_KEY": SERPER_API_KEY})
        st.markdown(f"### 🔍 Used Tool: {result['source']}")
        st.markdown(f"**Result:**\n\n{result['result']}")
        
        if use_memory:
            memory.add_memory(result["result"])