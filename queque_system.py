import streamlit as st
import pandas as pd

# ====== 跨stremlit版本rerun======
def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("您的 Streamlit 版本過舊，不支援 rerun！")

# ====== 排隊核心 ======
class FlexibleQueue:
    def __init__(self, queue_list, prep_limit=10, refill_threshold=5, refill_batch=5):
        self.full_list = list(queue_list)
        self.prep_limit = prep_limit
        self.refill_threshold = refill_threshold
        self.refill_batch = refill_batch

        self.called = None
        self.prep_queue = []
        self.done_list = []
        self.skipped_list = []
        self.pointer = 0

        self._initialize()

    def _initialize(self):
        n = min(self.prep_limit, len(self.full_list))
        self.prep_queue = self.full_list[:n]
        self.pointer = n
        self.called = None
        self.done_list = []
        self.skipped_list = []

    def call_next(self):
        # 移出一位進到號區
        if self.prep_queue:
            self.called = self.prep_queue.pop(0)
            self._maybe_refill()
        else:
            self.called = None

    def complete_and_next(self):
        # 將目前到號區號碼放到完成，再叫下一位
        if self.called is not None:
            self.done_list.append(self.called)
            self.call_next()

    def skip_and_next(self):
        # 將目前到號區號碼放到跳號，再叫下一位
        if self.called is not None:
            self.skipped_list.append(self.called)
            self.call_next()

    def recall_skip(self, idx):
    # 跳號名單補回準備區最前
        if 0 <= idx < len(self.skipped_list):
            n = self.skipped_list.pop(idx)
        self.prep_queue.insert(0, n)

    def _maybe_refill(self):
        if len(self.prep_queue) <= self.refill_threshold and self.pointer < len(self.full_list):
            n_add = min(self.refill_batch, self.prep_limit - len(self.prep_queue))
            for _ in range(n_add):
                if self.pointer < len(self.full_list):
                    self.prep_queue.append(self.full_list[self.pointer])
                    self.pointer += 1

    def reset(self):
        self._initialize()
        self.call_next()  # 初始化後直接叫第一位

# ====== Streamlit 主畫面 ======
st.set_page_config("叫號系統", layout="wide")
st.markdown("""
    <style>
        body { background-color: #191b1f; }
        .stApp { background-color: #191b1f; }
        .block-container { padding-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

st.title("叫號系統")

with st.expander("操作說明"):
    st.markdown("""
- 請以CSV匯入叫號順序
- 準備區為直向大字
- 主畫面焦點為到號區，顯示超大閃爍紅字
- 每次只叫1人，且只有你按下「完成」或「跳號」才會推進
- 跳號、完成分開顯示，跳號可叫回。
""")

file = st.file_uploader("匯入號碼名單（CSV，單欄）", type=["csv"])
prep_limit = st.number_input("準備區最大人數 N", min_value=1, max_value=100, value=10)
refill_threshold = st.number_input("批次補號門檻 Y（剩幾人時補）", min_value=1, max_value=prep_limit, value=5)
refill_batch = st.number_input("每次補號人數 Z", min_value=1, max_value=prep_limit, value=5)

# ---- 初始化隊列 ----
if (
    'queue' not in st.session_state
    or st.button("重啟系統")
    or 'need_reset' in st.session_state
):
    if file:
        df = pd.read_csv(file)
        if df.shape[1] == 1:
            input_list = df.iloc[:, 0].astype(str).tolist()
        else:
            col = st.selectbox("選擇號碼欄位", df.columns)
            input_list = df[col].astype(str).tolist()
    else:
        text = st.text_area("手動輸入號碼（每行一筆，順序即叫號順序）", height=150)
        input_list = [x.strip() for x in text.split('\n') if x.strip()]
    st.session_state.queue = FlexibleQueue(
        input_list,
        prep_limit=prep_limit,
        refill_threshold=refill_threshold,
        refill_batch=refill_batch
    )
    st.session_state.queue.reset()  # 初始化直接叫第一位
    if 'need_reset' in st.session_state:
        del st.session_state['need_reset']

queue: FlexibleQueue = st.session_state['queue']

# --- 操作主畫面 ---
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("<h2 style='text-align:left'>準備區</h2>", unsafe_allow_html=True)
    if queue.prep_queue:
        prep_html = "<div style='font-size:2.3em;line-height:1.7;font-weight:bold;color:#fff;text-align:left;padding-left:16px;'>"
        for n in queue.prep_queue:
            prep_html += f"{n}<br>"
        prep_html += "</div>"
        st.markdown(prep_html, unsafe_allow_html=True)
    else:
        st.info("目前準備區無號碼")

with col2:
    st.markdown("<h2 style='text-align:center'>到號區</h2>", unsafe_allow_html=True)
    if queue.called:
        st.markdown(
            f"""
            <style>
            .big-flash {{
                animation: flash 1s infinite;
                color: #ff2222;
                font-size: 13vw;
                font-weight: bold;
                text-align: center;
                margin-top: 40px;
                margin-bottom: 40px;
                letter-spacing:0.1em;
            }}
            @keyframes flash {{
                0%,100% {{ opacity: 1; }}
                50% {{ opacity: 0.4; }}
            }}
            </style>
            <div class="big-flash">{queue.called}</div>
            """,
            unsafe_allow_html=True
        )
        btn_col1, btn_col2 = st.columns([1, 1])
        if btn_col1.button("完成", key="done"):
            queue.complete_and_next()
            do_rerun()
        if btn_col2.button("跳號", key="skip"):
            queue.skip_and_next()
            do_rerun()
    else:
        if queue.prep_queue:
            st.info("請叫下一位")
            if st.button("叫下一位"):
                queue.call_next()
                do_rerun()
        else:
            st.warning("無可叫號名單")

st.divider()
col3, col4 = st.columns(2)
with col3:
    st.subheader("跳號名單")
    if queue.skipped_list:
        st.markdown(
            "<span style='font-size:1.6em; color:#eab308;'>" +
            "<br>".join(str(x) for x in queue.skipped_list) +
            "</span>", unsafe_allow_html=True
        )
        for idx, n in enumerate(queue.skipped_list):
            if st.button(f"叫回 {n}", key=f"recall_{idx}"):
                queue.recall_skip(idx)
                do_rerun()
    else:
        st.write("—")
with col4:
    st.subheader("已完成名單")
    if queue.done_list:
        st.markdown(
            "<span style='font-size:1.2em; color:#bbb;'>" +
            "<br>".join(str(x) for x in queue.done_list) +
            "</span>", unsafe_allow_html=True
        )
    else:
        st.write("—")
