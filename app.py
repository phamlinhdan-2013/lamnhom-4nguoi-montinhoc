import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit tối giản
st.set_page_config(page_title="Kiến Tha Đồ Ăn", page_icon="🐜", layout="centered")

# Mã nguồn game HTML5 + Javascript thời gian thực tích hợp Cửa hàng & Kỹ năng
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; justify-content: center; background-color: #f7f7f7; font-family: Arial, sans-serif; overflow: hidden; user-select: none; }
        canvas { background-color: #e5c158; border: 4px solid #8B4513; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .shop-btn { cursor: pointer; }
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
        let gameStatus = "START"; // START, PLAYING, WIN, GAMEOVER, SHOP, VICTORY
        let message = "Đi tìm thức ăn nào!";

        // Hệ thống Nhân vật & Cửa hàng
        let currentSkin = "🐜";
        let antSpeed = 4;
        let hasSuperPower = false;
        
        const skins = [
            { icon: "🐜", name: "Kiến Đen", price: 0, owned: true, speed: 4, power: false },
            { icon: "🌈", name: "Kiến Bảy Màu", price: 3, owned: false, speed: 4, power: false },
            { icon: "🌸", name: "Kiến Hồng", price: 3, owned: false, speed: 4, power: false },
            { icon: "👑", name: "Kiến To Cầu Vồng", price: 10, owned: false, speed: 5.5, power: true }
        ];

        // Đối tượng nhân vật trong game
        const ant = { x: 50, y: 350, size: 24, speed: 4 };
        const nest = { x: 50, y: 350, size: 30 };
        const food = { x: 520, y: 150, size: 25, type: "🍰", isCarried: false }; // Màn 1 bánh ở xa quái vật (y=150 thay vì 80)
        const monster = { x: 540, y: 50, size: 30, speed: 2, isActive: false, isDead: false };
        const trap = { x: 300, y: 200, size: 20, speedY: 3, dir: 1 };

        // Quản lý nút bấm
        const keys = {};
        window.addEventListener("keydown", e => { 
            keys[e.key] = true; 
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key)) e.preventDefault();
            
            // Xử lý chuyển màn bằng phím bất kỳ
            if(gameStatus === "START") { resetLevel("RESTART"); }
            else if(gameStatus === "WIN") { resetLevel("NEXT"); }
            else if(gameStatus === "GAMEOVER") { resetLevel("RESTART"); }
        });
        window.addEventListener("keyup", e => keys[e.key] = false);

        // Click chuột để tương tác Menu / Shop
        canvas.addEventListener("click", e => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            if (gameStatus === "START") {
                resetLevel("RESTART");
            } else if (gameStatus === "GAMEOVER" || gameStatus === "WIN" || gameStatus === "VICTORY") {
                // Bấm vào nút Mở Cửa Hàng
                if (mouseX >= 220 && mouseX <= 380 && mouseY >= 290 && mouseY <= 330) {
                    gameStatus = "SHOP";
                } else {
                    if (gameStatus === "WIN") resetLevel("NEXT");
                    else resetLevel("RESTART");
                }
            } else if (gameStatus === "SHOP") {
                // Bấm nút Quay Lại
                if (mouseX >= 20 && mouseX <= 100 && mouseY >= 350 && mouseY <= 380) {
                    gameStatus = "GAMEOVER";
                    return;
                }
                
                // Chọn mua vật phẩm trong cửa hàng
                for (let i = 0; i < skins.length; i++) {
                    let btnX = 60 + i * 130;
                    let btnY = 220;
                    if (mouseX >= btnX && mouseX <= btnX + 100 && mouseY >= btnY && mouseY <= btnY + 40) {
                        let s = skins[i];
                        if (s.owned) {
                            if (s.power) {
                                alert("Con kiến này có thể đè bẹp con quỷ");
                            }
                            currentSkin = s.icon;
                            ant.speed = s.speed;
                            hasSuperPower = s.power;
                        } else {
                            if (coins >= s.price) {
                                coins -= s.price;
                                s.owned = true;
                                if (s.power) {
                                    alert("Con kiến này có thể đè bẹp con quỷ");
                                }
                                currentSkin = s.icon;
                                ant.speed = s.speed;
                                hasSuperPower = s.power;
                            } else {
                                alert("Bạn không đủ số xu tích lũy để mua nhân vật này!");
                            }
                        }
                    }
                }
            }
        });

        function resetLevel(type) {
            if(type === "RESTART") { level = 1; coins = 0; }
            else if(type === "NEXT") { level++; }

            gameStatus = "PLAYING";
            ant.x = 50; ant.y = 350;
            food.isCarried = false;
            monster.x = 540; monster.y = 50;
            monster.isActive = false;
            monster.isDead = false;
            
            if(level === 1) { 
                food.type = "🍰"; 
                food.x = 450; food.y = 250; // Tránh xa góc quái vật
                monster.speed = 2.0; 
                message = "Màn 1: Quái vật đang ngủ. Hãy lén lấy Bánh ngọt!"; 
            }
            if(level === 2) { 
                food.type = "🍗"; 
                food.x = 520; food.y = 80;
                monster.speed = 2.4; 
                message = "Màn 2: Cẩn thận bẫy gai di chuyển cản đường mang Đùi gà về!"; 
            }
            if(level === 3) { 
                food.type = "🍭"; 
                food.x = 520; food.y = 80;
                monster.isActive = true; 
                monster.speed = 3.0; 
                message = "Màn 3: Quái vật tỉnh sẵn canh giữ Kẹo mút và đuổi cực nhanh!"; 
            }
            if(level > 3) { gameStatus = "VICTORY"; }
        }

        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.size && rect1.x + rect1.size > rect2.x &&
                   rect1.y < rect2.y + rect2.size && rect1.y + rect1.size > rect2.y;
        }

        function update() {
            if(gameStatus !== "PLAYING") return;

            // Di chuyển Kiến bằng phím mũi tên hoặc WASD
            if (keys["ArrowUp"] || keys["w"] || keys["W"]) ant.y = Math.max(40, ant.y - ant.speed);
            if (keys["ArrowDown"] || keys["s"] || keys["S"]) ant.y = Math.min(canvas.height - ant.size, ant.y + ant.speed);
            if (keys["ArrowLeft"] || keys["a"] || keys["A"]) ant.x = Math.max(0, ant.x - ant.speed);
            if (keys["ArrowRight"] || keys["d"] || keys["D"]) ant.x = Math.min(canvas.width - ant.size, ant.x + ant.speed);

            // Kiểm tra chạm thức ăn
            if(!food.isCarried && checkCollision(ant, food)) {
                food.isCarried = true;
                if (!monster.isDead) monster.isActive = true;
                message = "😱 Quái vật đuổi theo kìa! Mang đồ ăn chạy về TỔ mau!";
            }

            // Đồ ăn dính theo kiến
            if(food.isCarried) {
                food.x = ant.x;
                food.y = ant.y - 12;
            }

            // Quái vật đuổi theo
            if(monster.isActive && !monster.isDead) {
                let dx = ant.x - monster.x; let dy = ant.y - monster.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if(dist > 0) {
                    monster.x += (dx / dist) * monster.speed;
                    monster.y += (dy / dist) * monster.speed;
                }
            }

            // Hoạt động của Bẫy (Màn 2)
            if(level === 2) {
                trap.y += trap.speedY * trap.dir;
                if(trap.y < 60 || trap.y > 350) trap.dir *= -1;
                if(checkCollision(ant, trap)) { gameStatus = "GAMEOVER"; message = "💥 Bạn đã đạp trúng bẫy gai rồi!"; }
            }

            // Kiểm tra Quái vật chạm vào Kiến
            if(!monster.isDead && checkCollision(ant, monster)) {
                if (hasSuperPower) {
                    monster.isDead = true;
                    monster.isActive = false;
                    message = "💥 Kiến To Cầu Vồng xuất chiêu ĐÈ BẸP quái vật thành công!";
                } else {
                    gameStatus = "GAMEOVER";
                    message = "💀 Bạn đã bị Quái vật bắt mất tiêu!";
                }
            }

            // Kiểm tra về Tổ thành công
            if(food.isCarried && checkCollision(ant, nest)) {
                let reward = level === 1 ? 10 : (level === 2 ? 20 : 40);
                coins += reward;
                gameStatus = "WIN";
                message = `🎉 Tuyệt vời! Nhận được ${reward} xu. Click hoặc bấm phím để tiếp tục!`;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameStatus === "SHOP") {
                // Giao diện cửa hàng nhân vật
                ctx.fillStyle = "#333";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = "#ffcc00";
                ctx.font = "bold 26px Arial";
                ctx.fillText("🏪 CỬA HÀNG KIẾN", 200, 60);
                
                ctx.fillStyle = "#fff";
                ctx.font = "16px Arial";
                ctx.fillText(`Số xu tích lũy của bạn: ${coins} 💰`, 200, 100);
