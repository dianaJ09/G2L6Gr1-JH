import streamlit as st
import re

# 페이지 설정
st.set_page_config(
    page_title="Operation: Secret Code",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 2.5rem;
        color: #0f766e;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .game-container {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2dfdb 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .question-card {
        background: #f5eeda;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #a1887f;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .secret-code {
        font-family: 'Black Han Sans', sans-serif;
        font-size: 4rem;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .progress-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        border: 2px solid #374151;
        background-color: #9ca3af;
        color: white;
    }
    
    .progress-circle.solved {
        background-color: transparent;
        border-color: #10b981;
        box-shadow: 0 0 12px 2px #10b981;
    }
    
    .progress-circle.failed {
        background-color: #dc2626;
        border-color: #991b1b;
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    .riddle-box {
        background: #fef3c7;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #f59e0b;
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    .final-success {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 15px;
        color: white;
    }
    
    .final-success h2 {
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .final-success .trophy {
        font-size: 4rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 게임 데이터
QUESTIONS = [
    {
        "question": "1. 두 문장이 같은 의미가 되도록 할 때, 빈칸에 들어갈 알맞은 말은?\n\nShe is so bright that she can solve all the puzzles.\n= She is bright ______ _______ solve all the puzzles.",
        "answer": "enough to",
        "secret_code": "w",
        "color": "#ef4444"
    },
    {
        "question": "2. 문장에서 틀린 부분을 찾고, 전체 문장을 올바르게 고쳐 쓰세요.\n\n The candies are so deliciously that I keep eating them.",
        "answer": "The candies are so delicious that I keep eating them.",
        "secret_code": "t",
        "color": "#3b82f6"
    },
    {
        "question": "3. 우리말과 의미가 같도록 빈칸에 들어갈 알맞은 단어들을 쓰세요.\n\nThis building is (    )(    )(    ) it might fall down.\n(이 건물은 너무 낡아서 그것은 무너질지도 모른다.)",
        "answer": "so old that",
        "secret_code": "j",
        "color": "#22c55e"
    },
    {
        "question": "4. 우리말과 일치하도록 주어진 말과 so~that을 이용하여 문장을 완성해보세요.\n\n나는 너무 행복해서 하루 종일 노래를 불렀다. (happy/ sing)\nI was ________________ all day.",
        "answer": "so happy that I sang",
        "secret_code": "b",
        "color": "#eab308"
    },
    {
        "question": "5. 우리말과 일치하도록 주어진 말과 so~that을 이용하여 문장을 완성해보세요.\n\n이 문제들은 너무 쉬워서 나는 그것들을 쉽게 풀 수 있다. (These questions/easy/can)\n____________________ easily solve them.",
        "answer": "These questions are so easy that I can",
        "secret_code": "r",
        "color": "#8b5cf6"
    },
    {
        "question": "6. so that을 이용하여 다음 두 문장을 한 문장으로 고쳐 써 봅시다.\n\nThe wind was strong. It blew my hat off my head.\n= The wind was ________________________________.",
        "answer": "so strong that it blew my hat off my head.",
        "secret_code": "u",
        "color": "#ec4899"
    },
    {
        "question": "7. 빈칸에 들어갈 알맞은 말은? (번호만 쓰기)\n\n그 영화는 너무 무서워서 나는 그것을 보는 동안 소리를 질렀다.\nThe movie was ________ while watching it.\n\n(1) scary so I screamed that\n(2) so scary that I screamed\n(3) so scary I that screamed",
        "answer": "2",
        "secret_code": "q",
        "color": "#f97316"
    }
]

FINAL_SECRET_CODE = "wtjbruq"
RIDDLE = {
    "text": "I was born in the ocean.\nI am as white as snow.\nWhen I fall back into the water,\nI disappear without a trace.\n\nWhat am I?",
    "answer": "소금"
}

# 세션 상태 초기화
def initialize_session_state():
    """게임 상태를 초기화합니다."""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'attempts_left' not in st.session_state:
        st.session_state.attempts_left = 5
    if 'collected_codes' not in st.session_state:
        st.session_state.collected_codes = [None] * len(QUESTIONS)
    if 'game_phase' not in st.session_state:
        st.session_state.game_phase = 'start'  # start, question, final_code, riddle, success
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""
    if 'message' not in st.session_state:
        st.session_state.message = ""

def normalize_english_answer(text):
    """영어 답안을 정규화합니다."""
    return re.sub(r'[.,!]', '', text.lower().strip())

def normalize_korean_answer(text):
    """한국어 답안을 정규화합니다."""
    return text.strip()

def check_answer(user_answer, correct_answer):
    """답안을 확인합니다."""
    normalized_user = normalize_english_answer(user_answer)
    normalized_correct = normalize_english_answer(correct_answer)
    return normalized_user == normalized_correct

def render_progress_circles():
    """진행률 원형 표시기를 렌더링합니다."""
    cols = st.columns(len(QUESTIONS))
    for i, col in enumerate(cols):
        with col:
            if st.session_state.collected_codes[i] is not None:
                # 성공한 경우
                st.markdown(f"""
                <div class="progress-circle solved" style="border-color: {QUESTIONS[i]['color']}; box-shadow: 0 0 12px 2px {QUESTIONS[i]['color']};">
                    <span style="color: {QUESTIONS[i]['color']}; font-weight: bold;">{QUESTIONS[i]['secret_code'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.current_question > i:
                # 실패한 경우
                st.markdown("""
                <div class="progress-circle failed">
                    <span style="color: white; font-weight: bold;">X</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # 아직 시도하지 않은 경우
                st.markdown(f"""
                <div class="progress-circle">
                    <span style="color: white; font-weight: bold;">{i + 1}</span>
                </div>
                """, unsafe_allow_html=True)

def render_start_screen():
    """시작 화면을 렌더링합니다."""
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="game-container">
            <h2 style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">비밀 코드 작전</h2>
            <p style="text-align: center; font-size: 1.2rem; margin-bottom: 2rem;">
                바다 어딘가에 숨겨진 보물... 💎<br>
                7개의 문제를 풀어 비밀 코드를 모으고, 마지막 수수께끼를 해결하여 미션을 완수하라!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🚀 미션 시작!", key="start_button", use_container_width=True):
        st.session_state.game_phase = 'question'
        st.session_state.current_question = 0
        st.session_state.attempts_left = 5
        st.rerun()

def render_question_screen():
    """문제 화면을 렌더링합니다."""
    if st.session_state.current_question >= len(QUESTIONS):
        st.session_state.game_phase = 'final_code'
        st.rerun()
        return
    
    question_data = QUESTIONS[st.session_state.current_question]
    
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    
    # 진행률 표시
    render_progress_circles()
    
    with st.container():
        st.markdown(f"""
        <div class="question-card">
            <h3 style="color: #4f46e5; margin-bottom: 1rem;">문제 {st.session_state.current_question + 1}</h3>
            <div style="white-space: pre-wrap; font-size: 1.1rem; line-height: 1.6;">{question_data['question']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 답안 입력
    user_answer = st.text_input(
        "정답을 입력하세요:",
        value=st.session_state.user_answer,
        key=f"answer_input_{st.session_state.current_question}",
        placeholder="정답을 입력하세요..."
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("📝 제출", key=f"submit_{st.session_state.current_question}", use_container_width=True):
            if check_answer(user_answer, question_data['answer']):
                # 정답인 경우
                st.session_state.collected_codes[st.session_state.current_question] = question_data['secret_code']
                st.session_state.message = "정답입니다! 훌륭해요! 👍"
                st.session_state.game_phase = 'correct_answer'
            else:
                # 오답인 경우
                st.session_state.attempts_left -= 1
                if st.session_state.attempts_left > 0:
                    st.session_state.message = f"❌ 틀렸습니다. 다시 시도하세요! (남은 기회: {st.session_state.attempts_left}회)"
                else:
                    st.session_state.message = "❌ 시도 횟수를 모두 사용했습니다."
                    st.session_state.game_phase = 'failed_answer'
            st.rerun()
    
    with col2:
        if st.button("⏭️ 다음", key=f"skip_{st.session_state.current_question}", use_container_width=True):
            st.session_state.current_question += 1
            st.session_state.attempts_left = 5
            st.session_state.user_answer = ""
            st.session_state.message = ""
            st.rerun()
    
    # 메시지 표시
    if st.session_state.message:
        if "정답입니다" in st.session_state.message:
            st.markdown(f'<div class="success-message">{st.session_state.message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">{st.session_state.message}</div>', unsafe_allow_html=True)

def render_correct_answer_screen():
    """정답 화면을 렌더링합니다."""
    question_data = QUESTIONS[st.session_state.current_question]
    
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    render_progress_circles()
    
    with st.container():
        st.markdown(f"""
        <div class="question-card">
            <h3 style="text-align: center; color: #059669; margin-bottom: 1rem;">🎉 정답! 시크릿 코드를 획득했습니다!</h3>
            <div class="secret-code" style="color: {question_data['color']};">{question_data['secret_code'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("➡️ 다음 문제로", key="next_question", use_container_width=True):
        st.session_state.current_question += 1
        st.session_state.attempts_left = 5
        st.session_state.user_answer = ""
        st.session_state.message = ""
        st.session_state.game_phase = 'question'
        st.rerun()

def render_failed_answer_screen():
    """실패 화면을 렌더링합니다."""
    question_data = QUESTIONS[st.session_state.current_question]
    
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    render_progress_circles()
    
    with st.container():
        st.markdown(f"""
        <div class="question-card">
            <h3 style="text-align: center; color: #dc2626; margin-bottom: 1rem;">❌ 시도 횟수를 모두 사용했습니다.</h3>
            <p style="text-align: center; margin-bottom: 1rem;">이 문제의 시크릿 코드는 얻을 수 없습니다.</p>
            <p style="text-align: center; font-weight: bold; color: #374151;">정답은: {question_data['answer']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("➡️ 다음으로", key="next_after_failure", use_container_width=True):
        st.session_state.current_question += 1
        st.session_state.attempts_left = 5
        st.session_state.user_answer = ""
        st.session_state.message = ""
        st.session_state.game_phase = 'question'
        st.rerun()

def render_final_code_screen():
    """최종 코드 입력 화면을 렌더링합니다."""
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    render_progress_circles()
    
    with st.container():
        st.markdown("""
        <div class="question-card">
            <h3 style="text-align: center; margin-bottom: 1rem;">🔐 마지막 관문</h3>
            <p style="text-align: center; font-size: 1.1rem;">
                지금까지 획득한 7개의 시크릿 코드를 순서대로 입력하여 최종 수수께끼를 잠금 해제하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 획득한 코드 표시
    collected_codes = [code for code in st.session_state.collected_codes if code is not None]
    if collected_codes:
        st.markdown(f"**획득한 코드:** {''.join(collected_codes).upper()}")
    
    final_code = st.text_input(
        "시크릿 코드 7자리 입력:",
        key="final_code_input",
        placeholder="시크릿 코드 7자리 입력"
    )
    
    if st.button("🔓 잠금 해제", key="submit_final_code", use_container_width=True):
        if final_code.lower() == FINAL_SECRET_CODE:
            st.session_state.game_phase = 'riddle'
            st.rerun()
        else:
            st.error("코드가 일치하지 않습니다. 획득한 코드를 다시 확인해주세요.")

def render_riddle_screen():
    """수수께끼 화면을 렌더링합니다."""
    st.markdown('<h1 class="main-header">🧭 Operation: Secret Code</h1>', unsafe_allow_html=True)
    render_progress_circles()
    
    with st.container():
        st.markdown(f"""
        <div class="riddle-box">
            <h3 style="margin-bottom: 1rem;">📜 최종 수수께끼</h3>
            <div style="white-space: pre-wrap; font-size: 1.1rem; line-height: 1.6;">{RIDDLE['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    riddle_answer = st.text_input(
        "수수께끼의 정답은? (한국어):",
        key="riddle_answer_input",
        placeholder="수수께끼의 정답은? (한국어)"
    )
    
    if st.button("✅ 정답 확인", key="submit_riddle", use_container_width=True):
        if normalize_korean_answer(riddle_answer) == RIDDLE['answer']:
            st.session_state.game_phase = 'success'
            st.rerun()
        else:
            st.error("정답이 아닙니다. 수수께끼를 다시 한번 잘 생각해보세요.")

def render_success_screen():
    """성공 화면을 렌더링합니다."""
    st.markdown("""
    <div class="final-success">
        <h2>✨ 미션 성공! ✨</h2>
        <p style="font-size: 1.5rem; margin-bottom: 1rem;">축하합니다! 모든 비밀을 풀고 보물을 찾았습니다!</p>
        <div class="trophy">🏆 👑</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 다시 도전하기", key="restart", use_container_width=True):
        # 게임 상태 초기화
        for key in ['current_question', 'attempts_left', 'collected_codes', 'game_phase', 'user_answer', 'message']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def main():
    """메인 함수"""
    initialize_session_state()
    
    # 게임 단계에 따른 화면 렌더링
    if st.session_state.game_phase == 'start':
        render_start_screen()
    elif st.session_state.game_phase == 'question':
        render_question_screen()
    elif st.session_state.game_phase == 'correct_answer':
        render_correct_answer_screen()
    elif st.session_state.game_phase == 'failed_answer':
        render_failed_answer_screen()
    elif st.session_state.game_phase == 'final_code':
        render_final_code_screen()
    elif st.session_state.game_phase == 'riddle':
        render_riddle_screen()
    elif st.session_state.game_phase == 'success':
        render_success_screen()

if __name__ == "__main__":
    main()
