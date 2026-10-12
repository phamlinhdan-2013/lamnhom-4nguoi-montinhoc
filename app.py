import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit tối giản nhất có thể
st.set_page_config(page_title="Dino Chrome Game Pro", page_icon="🦖", layout="centered")

# Đoạn mã game HTML5 + Canvas + Javascript chuyển động thời gian thực mượt mà
dino_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; display: flex; justify-content: center; align-items: center; background-color: #f7f7f7; font-family: Arial, sans-serif; overflow: hidden; user-select: none; }
        canvas { background-color: #fff; border: 2px solid #535353; border-radius: 8px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="200"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gameSpeed = 5;
        let score = 0;
        let highScore = 0;
        let isGameOver = false;

        const dino = {
            x: 50,
            y: 160,
            width: 25,
            height: 30,
            gravity: 0.6,
            jumpForce: -10,
            velocity: 0,
            isJumping: false
        };

        let obstacles = [];
        let spawnTimer = 0;

        function jump() {
            if (isGameOver) {
                resetGame();
                return;
            }
            if (!dino.isJumping) {
                dino.velocity = dino.jumpForce;
                dino.isJumping = true;
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
            let height = Math.random() > 0.5 ? 40 : 30;
            let width = 15;
            obstacles.push({
                x: canvas.width,
                y: 190 - height,
                width: width,
                height: height
            });
        }

        function resetGame() {
            obstacles = [];
            score = 0;
            gameSpeed = 5;
            isGameOver = false;
            dino.y = 160;
            dino.velocity = 0;
            dino.isJumping = false;
            animate();
        }

        let animationFrameId;
        function animate() {
            if (isGameOver) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            dino.velocity += dino.gravity;
            dino.y += dino.velocity;

            if (dino.y >= 160) {
                dino.y = 160;
                dino.velocity = 0;
                dino.isJumping = false;
            }

            ctx.font = "26px Arial";
            ctx.fillText("🦖", dino.x, dino.y + 24);

            spawnTimer++;
            if (spawnTimer > Math.max(50, 100 - gameSpeed * 3)) {
                spawnObstacle();
                spawnTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                let o = obstacles[i];
                o.x -= gameSpeed;

                ctx.font = "24px Arial";
                ctx.fillText("🌵", o.x, o.y + 24);

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
                    if (score % 5 === 0) gameSpeed += 0.5; 
                }
            }

            ctx.fillStyle = "#535353";
            ctx.font = "16px monospace";
            ctx.fillText("HI " + String(highScore).padStart(5, '0') + "   " + String(score).padStart(5, '0'), 460, 30);

            if (isGameOver) {
                ctx.fillStyle = "#535353";
                ctx.font = "bold 20px monospace";
                ctx.fillText("G A M E   O V E R", 220, 90);
                ctx.font = "14px Arial";
                ctx.fillText("💀 Bấm chuột hoặc nút Cách để chơi lại", 185, 120);
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

components.html(dino_game_html, height=220, scrolling=False)
