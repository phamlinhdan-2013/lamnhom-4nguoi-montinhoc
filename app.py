import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit tối giản nhất có thể
st.set_page_config(page_title="Dino Chrome Game Pro Max", page_icon="🦖", layout="centered")

# Đoạn mã game HTML5 Canvas to hơn + Hiệu ứng Đổi màu + Âm thanh khi nhảy
dino_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; display: flex; justify-content: center; align-items: center; background-color: #f7f7f7; font-family: Arial, sans-serif; overflow: hidden; user-select: none; }
        canvas { background-color: #fff; border: 3px solid #333; border-radius: 12px; box-shadow: 0px 6px 20px rgba(0,0,0,0.15); }
    </style>
</head>
<body>
    <!-- Phóng to kích thước Canvas lên 800x400 -->
    <canvas id="gameCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gameSpeed = 6;
        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        
        // Mảng chứa các màu sắc ngẫu nhiên cho Khủng long
        const colors = ["#535353", "#ff3333", "#33cc33", "#3333ff", "#ff9900", "#cc33ff", "#00ffff", "#ff3399"];
        let currentDinoColor = colors[0];

        // Khởi tạo Khủng long (Điều chỉnh lại tọa độ theo khung màn hình 400px)
        const dino = {
            x: 80,
            y: 330,
            width: 40,
            height: 50,
            gravity: 0.6,
            jumpForce: -13,
            velocity: 0,
            isJumping: false
        };

        let obstacles = [];
        let spawnTimer = 0;

        // Hàm tự tạo âm thanh kỹ thuật số phát qua loa máy tính khi nhảy
        function playJumpSound() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                
                oscillator.type = 'sine';
                oscillator.frequency.setValueAtTime(150, audioCtx.currentTime); // Tần số âm thanh lúc bắt đầu nhảy
                oscillator.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.12); // Âm thanh vút lên cao
                
                gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
                
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.12);
            } catch (e) {
                console.log("Trình duyệt chặn âm thanh tự động");
            }
        }

        function jump() {
            if (isGameOver) {
                resetGame();
                return;
            }
            if (!dino.isJumping) {
                dino.velocity = dino.jumpForce;
                dino.isJumping = true;
                playJumpSound(); // Phát âm thanh "Típ" khi nhảy
            }
        }

        window.addEventListener("keydown", function(e) {
            if (e.code === "Space") {
                e.preventDefault();
                jump();
            }
        });

        canvas.addEventListener("click", jump);

        function spawnObstacle() {
            let height = Math.random() > 0.5 ? 65 : 45;
            let width = 22;
            obstacles.push({
                x: canvas.width,
                y: 380 - height,
                width: width,
                height: height
            });
        }

        function resetGame() {
            obstacles = [];
            score = 0;
            gameSpeed = 6;
            isGameOver = false;
            currentDinoColor = colors[0];
            dino.y = 330;
            dino.velocity = 0;
            dino.isJumping = false;
            animate();
        }

        let animationFrameId;
        function animate() {
            if (isGameOver) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ mặt đất gạch chân cố định dưới chân khủng long
            ctx.strokeStyle = "#535353";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 380);
            ctx.lineTo(canvas.width, 380);
            ctx.stroke();

            // Áp dụng trọng lực cho Khủng long
            dino.velocity += dino.gravity;
            dino.y += dino.velocity;

            if (dino.y >= 330) {
                dino.y = 330;
                dino.velocity = 0;
                dino.isJumping = false;
            }

            // Vẽ Khủng long (Dạng Emoji to hơn kèm theo màu nền đổi màu sinh động)
            ctx.save();
            ctx.font = "42px Arial";
            // Tạo hiệu ứng đổ bóng màu để con khủng long đổi màu liên tục xung quanh
            ctx.shadowBlur = 15;
            ctx.shadowColor = currentDinoColor;
            ctx.fillStyle = currentDinoColor;
            ctx.fillText("🦖", dino.x, dino.y + 38);
            ctx.restore();

            // Quản lý vật cản Xương rồng lao tới
            spawnTimer++;
            if (spawnTimer > Math.max(45, 95 - gameSpeed * 3)) {
                spawnObstacle();
                spawnTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                let o = obstacles[i];
                o.x -= gameSpeed;

                // Vẽ Xương rồng to rõ ràng hơn
                ctx.font = "38px Arial";
                ctx.fillText("🌵", o.x, o.y + 35);

                // Kiểm tra va chạm (Đâm vào xương rồng)
                if (
                    dino.x < o.x + o.width &&
                    dino.x + dino.width > o.x &&
                    dino.y < o.y + o.height &&
                    dino.y + dino.height > o.y
                ) {
                    isGameOver = true;
                }

                // Khi vượt qua xương rồng thành công: Cộng điểm + Đổi màu khủng long
                if (o.x + o.width < 0) {
                    obstacles.splice(i, 1);
                    score++;
                    
                    // Thực hiện đổi màu ngẫu nhiên từ mảng màu có sẵn
                    let randomColorIndex = Math.floor(Math.random() * colors.length);
                    currentDinoColor = colors[randomColorIndex];
                    
                    if (score > highScore) highScore = score;
                    if (score % 4 === 0) gameSpeed += 0.5; // Tăng dần tốc độ
                }
            }

            // Hiển thị bảng điểm chữ lớn rõ ràng
            ctx.fillStyle = "#535353";
            ctx.font = "bold 20px monospace";
            ctx.fillText("HI " + String(highScore).padStart(5, '0') + "   " + String(score).padStart(5, '0'), 600, 45);

            // Giao diện Game Over khi thua cuộc
            if (isGameOver) {
                ctx.fillStyle = "#333";
                ctx.font = "bold 32px monospace";
                ctx.fillText("G A M E   O V E R", 260, 180);
                ctx.font = "18px Arial";
                ctx.fillText("💀 Bấm chuột hoặc nút Cách để chơi lại", 245, 230);
                cancelAnimationFrame(animationFrameId);
                return;
            }

            animationFrameId = requestAnimationFrame(animate);
        }

        // Bắt đầu chạy game
        animate();
    </script>
</body>
</html>
"""

# Tăng kích thước nhúng chiều rộng và chiều cao lên để chứa vừa khít Canvas 800x400
components.html(dino_game_html, width=820, height=430, scrolling=False)
