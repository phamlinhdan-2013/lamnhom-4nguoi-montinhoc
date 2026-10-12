import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit tối giản nhất có thể
st.set_page_config(page_title="Ant Adventure Game", page_icon="🐜", layout="centered")

# Mã nguồn game HTML5 + Javascript thời gian thực
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; justify-content: center; background-color: #f7f7f7; font-family: monospace; overflow: hidden; }
        canvas { background-color: #e5c158; border: 4px solid #8B4513; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Trạng thái hệ thống
        let level = 1;
        let coins = 0;
        let gameStatus = "START"; // START, PLAYING, WIN, GAMEOVER
        let message = "Đi tìm thức ăn nào!";

        // Đối tượng nhân vật
        const ant = { x: 50, y: 350, size: 20, speed: 4 };
        const nest = { x: 50, y: 350, size: 30 };
        const food = { x: 520, y: 80, size: 25, type: "🍰", isCarried: false };
        const monster = { x: 540, y: 50, size: 30, speed: 2, isActive: false, color: "#990000" };
        const trap = { x: 300, y: 200, size: 20, speedY: 3, dir: 1 };

        // Quản lý nút bấm bàn phím
        const keys = {};
        window.addEventListener("keydown", e => { 
            keys[e.key] = true; 
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key)) e.preventDefault();
            if(gameStatus !== "PLAYING") resetLevel(gameStatus === "WIN" ? "NEXT" : "RESTART");
        });
        window.addEventListener("keyup", e => keys[e.key] = false);

        function resetLevel(type) {
            if(type === "RESTART") { level = 1; coins = 0; }
            else if(type === "NEXT") { level++; }

            gameStatus = "PLAYING";
            ant.x = 50; ant.y = 350;
            food.x = 520; food.y = 80;
            food.isCarried = false;
            monster.x = 540; monster.y = 50;
            
            if(level === 1) { food.type = "🍰"; monster.isActive = false; monster.speed = 2.2; message = "Màn 1: Quái vật đang ngủ. Hãy lén lấy Bánh ngọt!"; }
            if(level === 2) { food.type = "🍗"; monster.isActive = false; monster.speed = 2.5; message = "Màn 2: Cẩn thận bẫy gai trên đường mang Đùi gà về!"; }
            if(level === 3) { food.type = "🍭"; monster.isActive = true; monster.speed = 3.2; message = "Màn 3: Quái vật tỉnh sẵn và chạy nhanh hơn để canh Kẹo mút!"; }
            if(level > 3) { gameStatus = "VICTORY"; }
        }

        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.size && rect1.x + rect1.size > rect2.x &&
                   rect1.y < rect2.y + rect2.size && rect1.y + rect1.size > rect2.y;
        }

        function update() {
            if(gameStatus !== "PLAYING") return;

            // Di chuyển Kiến bằng phím mũi tên hoặc WASD
            if (keys["ArrowUp"] || keys["w"] || keys["W"]) ant.y = Math.max(0, ant.y - ant.speed);
            if (keys["ArrowDown"] || keys["s"] || keys["S"]) ant.y = Math.min(canvas.height - ant.size, ant.y + ant.speed);
            if (keys["ArrowLeft"] || keys["a"] || keys["A"]) ant.x = Math.max(0, ant.x - ant.speed);
            if (keys["ArrowRight"] || keys["d"] || keys["D"]) ant.x = Math.min(canvas.width - ant.size, ant.x + ant.speed);

            // Kiểm tra chạm thức ăn
            if(!food.isCarried && checkCollision(ant, food)) {
                food.isCarried = true;
                monster.isActive = true;
                message = "😱 Quái vật thức giấc rồi! Chạy về TỔ mau!";
            }

            // Nếu đang mang thức ăn, đồ ăn sẽ dính theo kiến
            if(food.isCarried) {
                food.x = ant.x;
                food.y = ant.y - 10;
            }

            // Quái vật đuổi theo khi tỉnh giấc
            if(monster.isActive) {
                let targetX = ant.x; let targetY = ant.y;
                let dx = targetX - monster.x; let dy = targetY - monster.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if(dist > 0) {
                    monster.x += (dx / dist) * monster.speed;
                    monster.y += (dy / dist) * monster.speed;
                }
            }

            // Hoạt động của Bẫy (Chỉ có ở Màn 2)
            if(level === 2) {
                trap.y += trap.speedY * trap.dir;
                if(trap.y < 50 || trap.y > 330) trap.dir *= -1;
                if(checkCollision(ant, trap)) { gameStatus = "GAMEOVER"; message = "💥 Bạn đã đạp trúng bẫy gai!"; }
            }

            // Kiểm tra Quái vật bắt được Kiến
            if(checkCollision(ant, monster)) {
                gameStatus = "GAMEOVER";
                message = "💀 Bạn đã bị Quái vật bắt mất tiêu!";
            }

            // Kiểm tra về Tổ thành công
            if(food.isCarried && checkCollision(ant, nest)) {
                let reward = level === 1 ? 10 : (level === 2 ? 20 : 40);
                coins += reward;
                gameStatus = "WIN";
                message = `🎉 Thành công! Nhận được ${reward} xu. Bấm phím bất kỳ để tiếp tục!`;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Tổ kiến
            ctx.font = "35px Arial";
            ctx.fillText("🕳️", nest.x, nest.y + 10);
            ctx.fillStyle = "#8B4513";
            ctx.font = "12px Arial";
            ctx.fillText("TỔ KIẾN", nest.x - 5, nest.y + 25);

            // Vẽ Kiến
            ctx.font = "24px Arial";
            ctx.fillText("🐜", ant.x, ant.y + 15);

            // Vẽ Thức ăn
            if(gameStatus === "PLAYING" || gameStatus === "GAMEOVER") {
                ctx.font = "24px Arial";
                ctx.fillText(food.type, food.x, food.y + 15);
            }

            // Vẽ Quái vật
            ctx.font = "32px Arial";
            ctx.fillText(monster.isActive ? "👹" : "😴", monster.x, monster.y + 20);

            // Vẽ Bẫy (Màn 2)
            if(level === 2 && gameStatus === "PLAYING") {
                ctx.font = "24px Arial";
                ctx.fillText("💥", trap.x, trap.y + 15);
            }

            // Hiển thị UI Bảng điểm phía trên
            ctx.fillStyle = "#333";
            ctx.fillRect(0, 0, canvas.width, 40);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 14px monospace";
            ctx.fillText(`MÀN: ${level}  |  XU: ${coins}💰`, 20, 25);
            ctx.font = "12px Arial";
            ctx.fillText(message, 210, 25);

            // Giao diện các màn hình trạng thái
            ctx.fillStyle = "rgba(0,0,0,0.7)";
            ctx.font = "bold 24px monospace";
            
            if(gameStatus === "START") {
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#fff";
                ctx.fillText("TRÒ CHƠI: KIẾN CHĂM CHỈ", 150, 180);
                ctx.font = "14px Arial";
                ctx.fillText("Bấm phím bất kỳ để BẮT ĐẦU chơi nhé!", 160, 230);
            } else if(gameStatus === "GAMEOVER") {
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff4d4d";
                ctx.fillText("G A M E   O V E R", 200, 180);
                ctx.fillStyle = "#fff";
                ctx.font = "14px Arial";
                ctx.fillText("Bấm phím bất kỳ để CHƠI LẠI từ đầu", 175, 230);
            } else if(gameStatus === "VICTORY") {
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#4dff4d";
                ctx.fillText("🏆 CHIẾN THẮNG HOÀN TOÀN! 🏆", 140, 160);
                ctx.fillStyle = "#fff";
                ctx.font = "18px monospace";
                ctx.fillText(`Tổng số xu tích lũy: ${coins} 💰`, 180, 210);
                ctx.font = "14px Arial";
                ctx.fillText("Bạn đã vượt qua toàn bộ thử thách xuất sắc!", 160, 260);
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Nhúng game vào Streamlit với chiều cao vừa khít khung canvas
components.html(game_html, height=410, scrolling=False)
