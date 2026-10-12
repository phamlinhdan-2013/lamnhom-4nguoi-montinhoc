import streamlit as st
import random
import time

# Cấu hình giao diện trang web game
st.set_page_config(page_title="Dino Jump Game", page_icon="🦖", layout="centered")

st.title("🦖 Game Khủng Long Vượt Xương Rồng")
st.write("Giải pháp làm game Dino huyền thoại chạy mượt mà trên nền tảng Streamlit!")

# Khởi tạo các biến lưu trạng thái game (Session State)
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.high_score = 0
    st.session_state.cactus_distance = random.randint(2, 5)  # Khoảng cách đến cây xương rồng (tính bằng mét)
    st.session_state.game_over = False
    st.session_state.log_message = "Trò chơi bắt đầu! Hãy chuẩn bị nhảy."

# Hàm xử lý khi người chơi bấm nút Nhảy
def play_turn(jump_force):
    if st.session_state.game_over:
        return

    # Cây xương rồng tiến lại gần hơn từ 1 đến 3 mét ngẫu nhiên
    speed = random.randint(1, 3)
    st.session_state.cactus_distance -= speed

    # Kiểm tra va chạm hoặc vượt qua thành công
    if st.session_state.cactus_distance <= 0:
        # Nếu khoảng cách bằng hoặc nhỏ hơn 0, người chơi phải nhảy đủ cao/xa để qua
        if jump_force >= 2:  # Cần lực nhảy từ "Vừa" trở lên
            st.session_state.score += 10
            st.session_state.log_message = f"🎉 Tuyệt vời! Bạn đã nhảy qua cây xương rồng! (+10 điểm)"
            st.session_state.cactus_distance = random.randint(3, 6) # Tạo cây xương rồng mới phía xa
        else:
            st.session_state.game_over = True
            st.session_state.log_message = "💥 Đoàng! Lực nhảy quá yếu, bạn đã đâm vào cây xương rồng!"
    else:
        # Xương rồng chưa tới nơi
        if jump_force > 0:
            st.session_state.log_message = f"💨 Bạn nhảy hơi sớm! Cây xương rồng vẫn còn cách {st.session_state.cactus_distance} mét."
        else:
            st.session_state.score += 2
            st.session_state.log_message = f"🏃 Bạn tiếp tục chạy an toàn. Xương rồng còn cách {st.session_state.cactus_distance} mét. (+2 điểm)"

    # Cập nhật Điểm Kỷ Lục
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

# Hàm chơi lại game
def reset_game():
    st.session_state.score = 0
    st.session_state.cactus_distance = random.randint(3, 6)
    st.session_state.game_over = False
    st.session_state.log_message = "Trò chơi đã được đặt lại. Chạy thôi!"

# --- GIAO DIỆN HIỂN THỊ GAME ---

# 1. Bảng điểm số
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🎯 Điểm số hiện tại", value=st.session_state.score)
with col2:
    st.metric(label="🏆 Điểm kỷ lục", value=st.session_state.high_score)

# 2. Đồ họa giả lập bằng văn bản & Emoji
st.write("---")
dino_status = "🦖 (Đang nhảy)" if st.session_state.log_message.startswith("🎉") or st.session_state.log_message.startswith("💨") else "🦖"
if st.session_state.game_over:
    dino_status = "💀 (Thua cuộc)"

# Tạo đường chạy trực quan
track = "_" * 20
cactus_pos = max(0, min(19, st.session_state.cactus_distance * 3))
track_list = list(track)
if not st.session_state.game_over:
    track_list[cactus_pos] = "🌵"
track_display = "".join(track_list)

st.subheader(f"{dino_status} {track_display}")
st.write("---")

# 3. Khu vực điều khiển hành động
if not st.session_state.game_over:
    st.info(st.session_state.log_message)
    
    # Người chơi chọn lực nhảy
    choice = st.radio("Chọn hành động cho lượt này:", ["Tiếp tục chạy (Không nhảy)", "Nhảy vừa phải", "Nhảy cực mạnh"])
    
    # Áp dụng lực nhảy tương ứng
    force_map = {"Tiếp tục chạy (Không nhảy)": 0, "Nhảy vừa phải": 2, "Nhảy cực mạnh": 3}
    
    if st.button("Xác nhận hành động 🚀"):
        play_turn(force_map[choice])
        st.rerun()
else:
    st.error(st.session_state.log_message)
    st.button("🎮 Chơi lại từ đầu", on_click=reset_game)

   
 
