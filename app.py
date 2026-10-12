import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit tối giản nhất có thể
st.set_page_config(page_title="Dino Chrome Game RGB Real", page_icon="🦖", layout="centered")

# Đoạn mã game HTML5 Canvas to + Thân Khủng long tự đổi màu liên tục sắc nét + Âm thanh khi nhảy
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
    <canvas id="gameCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gameSpeed = 6;
        let score = 0;
        let highScore = 0;
        let isGameOver = false;
        
        // Biến tăng dần để tính toán màu sắc cầu vồng của thân khủng long
        let hueColor = 0;

        // Khởi tạo Khủng long (Chỉnh lại kích thước chuẩn để vẽ đồ họa hình dáng)
        const dino = {
            x: 80,
            y: 330,
            width: 44,
            height: 47,
            gravity: 0.6,
            jumpForce: -13,
            velocity: 0,
            isJumping: false
        };

        let obstacles =;
        let spawnTimer = 0;

        function playJumpSound() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                
                oscillator.type = 'sine';
                oscillator.frequency.setValueAtTime(150, audioCtx.currentTime); 
                oscillator.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.12); 
                
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
                playJumpSound(); 
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

        // Hàm tự vẽ chú khủng long Dino bằng các khối hình học (được đổi màu chính xác thân thể)
        function drawDino(x, y, color) {
            ctx.fillStyle = color;
            
            // Đầu và mỏ khủng long
            ctx.fillRect(x + 20, y, 24, 12);
            ctx.fillRect(x + 16, y + 4, 4, 8);
            ctx.fillRect(x + 20, y + 12, 16, 4);
            
            // Mắt (Màu trắng sắc nét)
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(x + 24, y + 3, 3, 3);
            ctx.fillStyle = color;

            // Cổ và thân hình
            ctx.fillRect(x + 16, y + 16, 12, 4);
            ctx.fillRect(x + 8, y + 20, 20, 16);
            ctx.fillRect(x, y + 24, 8, 8); // Đuôi cất cao
            ctx.fillRect(x, y + 20, 4, 4);

            // Chân trái và chân phải
            ctx.fillRect(x + 12, y + 36, 4, 8);
            ctx.fillRect(x + 20, y + 36, 4, 8);
            ctx.fillRect(x + 10, y + 44, 6, 3);
            ctx.fillRect(x + 18, y + 44, 6, 3);
        }

        function resetGame() {
            obstacles =;
            score = 0;
            gameSpeed = 6;
            isGameOver = false;
            hueColor = 0;
            dino.y = 330;
            dino.velocity = 0;
            dino.isJumping = false;
            animate();
        }

        let animationFrameId;
        function animate() {
            if (isGameOver) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ mặt đất cố định dưới chân
            ctx.strokeStyle = "#535353";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 380);
            ctx.lineTo(canvas.width, 380);
            ctx.stroke();

            // Áp dụng trọng lực cho Khủng long
            dino.velocity += dino.gravity;
            dino.y += dino.velocity;

            if (dino.y >= 333) {
                dino.y = 333;
                dino.velocity = 0;
                dino.isJumping = false;
            }

            // TỰ ĐỘNG ĐỔI MÀU THÂN: Tăng góc màu sắc cầu vồng sau mỗi khung hình
            hueColor = (hueColor + 2) % 360; 
            let dynamicColor = `hsl(${hueColor}, 95%, 45%)`;

            // Gọi hàm vẽ khủng long tự đổi màu sắc nét (Không bị bóng mờ xung quanh)
            drawDino(dino.x, dino.y, dynamicColor);

            // Quản lý vật cản Xương rồng lao tới
            spawnTimer++;
            if (spawnTimer > Math.max(45, 95 - gameSpeed * 3)) {
                spawnObstacle();
                spawnTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                let o = obstacles[i];
                o.x -= gameSpeed;

                // Vẽ Xương rồng màu xám tối chuẩn cổ điển
                ctx.font = "38px Arial";
                ctx.fillStyle = "#535353"; 
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

                if (o.x + o.width < 0) {
                    obstacles.splice(i, 1);
                    score++;
                    
                    if (score > highScore) highScore = score;
                    if (score % 4 === 0) gameSpeed += 0.5; 
                }
            }

            // Hiển thị bảng điểm
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

        animate();
    </script>
</body>
</html>
"""

components.html(dino_game_html, width=820, height=430, scrolling=False)
