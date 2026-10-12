import streamlit st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit gọn gàng nhất
st.set_page_config(page_title="Kiến Tha Đồ Ăn", page_icon="🐜", layout="centered")

# Mã nguồn game HTML5 + Javascript thời gian thực hoàn chỉnh không lỗi
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; display: flex; justify-content: center; background-color: #f7f7f7; font-family: Arial, sans-serif; overflow: hidden; user-select: none; }
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
        let gameStatus = "START"; 
        let message = "Đi tìm thức ăn nào!";

        // Hệ thống Cửa hàng & Nhân vật
        let currentSkin = "🐜";
        let hasSuperPower = false;
        
        const skins = [
            { icon: "🐜", name: "Kiến Đen", price: 0, owned: true, speed: 4, power: false },
            { icon: "🌈", name: "Kiến Bảy Màu", price: 3, owned: false, speed: 4, power: false },
            { icon: "🌸", name: "Kiến Hồng", price: 3, owned: false, speed: 4, power: false },
            { icon: "👑", name: "Kiến To Cầu Vồng", price: 10, owned: false, speed: 5.5, power: true }
        ];

        // Khởi tạo các đối tượng game
        const ant = { x: 50, y: 350, size: 24 };
        const nest = { x: 50, y: 350, size: 30 };
        const food = { x: 450, y: 250, size: 25, type: "🍰", isCarried: false }; 
        const monster = { x: 540, y: 50, size: 30, speed: 2, isActive: false, isDead: false };
        const trap = { x: 300, y: 200, size: 20, speedY: 3, dir: 1 };

        // Xử lý nút bấm bàn phím di chuyển
        const keys = {};
        window.addEventListener("keydown", e => { 
            keys[e.key] = true; 
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key)) e.preventDefault();
            
            if(gameStatus === "START") { resetLevel("RESTART"); }
            else if(gameStatus === "GAMEOVER" || gameStatus === "VICTORY") { resetLevel("RESTART"); }
            else if(gameStatus === "WIN") { resetLevel("NEXT"); }
        });
        window.addEventListener("keyup", e => keys[e.key] = false);

        // Chuột click chọn Menu / Shop
        canvas.addEventListener("click", e => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            if (gameStatus === "START") {
                resetLevel("RESTART");
            } else if (gameStatus === "GAMEOVER" || gameStatus === "WIN" || gameStatus === "VICTORY") {
                // Click nút vào Cửa Hàng
                if (mouseX >= 220 && mouseX <= 380 && mouseY >= 210 && mouseY <= 250) {
                    gameStatus = "SHOP";
                } 
                // Click nút Chơi Tiếp / Chơi Lại
                else if (mouseX >= 220 && mouseX <= 380 && mouseY >= 260 && mouseY <= 300) {
                    if (gameStatus === "WIN") resetLevel("NEXT");
                    else resetLevel("RESTART");
                }
            } else if (gameStatus === "SHOP") {
                // Click nút Quay Lại
                if (mouseX >= 20 && mouseX <= 100 && mouseY >= 350 && mouseY <= 380) {
                    gameStatus = "GAMEOVER";
                    return;
                }
                
                // Mua và chọn skin kiến
                for (let i = 0; i < skins.length; i++) {
                    let btnX = 50 + i * 130;
                    let btnY = 280;
                    if (mouseX >= btnX && mouseX <= btnX + 100 && mouseY >= btnY && mouseY <= btnY + 30) {
                        let s = skins[i];
                        if (s.owned) {
                            if (s.power) alert("Con kiến này có thể đè bẹp con quỷ");
                            currentSkin = s.icon;
                            hasSuperPower = s.power;
                        } else {
                            if (coins >= s.price) {
                                coins -= s.price;
                                s.owned = true;
                                if (s.power) alert("Con kiến này có thể đè bẹp con quỷ");
                                currentSkin = s.icon;
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

            if(level > 3) { gameStatus = "VICTORY"; return; }

            gameStatus = "PLAYING";
            ant.x = 50; ant.y = 350;
            food.isCarried = false;
            monster.x = 540; monster.y = 50;
            monster.isDead = false;
            
            if(level === 1) { 
                food.type = "🍰"; 
                food.x = 450; food.y = 250; 
                monster.isActive = false;
                monster.speed = 2.0; 
                message = "Màn 1: Quái vật đang ngủ. Hãy lén lấy Bánh ngọt!"; 
            }
            if(level === 2) { 
                food.type = "🍗"; 
                food.x = 520; food.y = 80;
                monster.isActive = false;
                monster.speed = 2.4; 
                message = "Màn 2: Cẩn thận bẫy gai di chuyển mang Đùi gà về!"; 
            }
            if(level === 3) { 
                food.type = "🍭"; 
                food.x = 520; food.y = 80;
                monster.isActive = true; 
                monster.speed = 3.0; 
                message = "Màn 3: Quái vật tỉnh sẵn canh giữ Kẹo mút!"; 
            }
        }

        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.size && rect1.x + rect1.size > rect2.x &&
                   rect1.y < rect2.y + rect2.size && rect1.y + rect1.size > rect2.y;
        }

        function update() {
            if(gameStatus !== "PLAYING") return;

            let currentSpeed = hasSuperPower ? 5.5 : 4;

            // Di chuyển
            if (keys["ArrowUp"] || keys["w"] || keys["W"]) ant.y = Math.max(40, ant.y - currentSpeed);
            if (keys["ArrowDown"] || keys["s"] || keys["S"]) ant.y = Math.min(canvas.height - ant.size, ant.y + currentSpeed);
            if (keys["ArrowLeft"] || keys["a"] || keys["A"]) ant.x = Math.max(0, ant.x - currentSpeed);
            if (keys["ArrowRight"] || keys["d"] || keys["D"]) ant.x = Math.min(canvas.width - ant.size, ant.x + currentSpeed);

            // Nhặt thức ăn
            if(!food.isCarried && checkCollision(ant, food)) {
                food.isCarried = true;
                if (!monster.isDead) monster.isActive = true;
                message = "😱 Quái vật đuổi theo kìa! Chạy về TỔ mau!";
            }

            if(food.isCarried) {
                food.x = ant.x;
                food.y = ant.y - 12;
            }

            // Quái vật đuổi theo kiến
            if(monster.isActive && !monster.isDead) {
                let dx = ant.x - monster.x; let dy = ant.y - monster.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if(dist > 0) {
                    monster.x += (dx / dist) * monster.speed;
                    monster.y += (dy / dist) * monster.speed;
                }
            }

            // Hoạt động bẫy gai (Màn 2)
            if(level === 2) {
                trap.y += trap.speedY * trap.dir;
                if(trap.y < 60 || trap.y > 350) trap.dir *= -1;
                if(checkCollision(ant, trap)) { gameStatus = "GAMEOVER"; message = "💥 Bạn đã đạp trúng bẫy gai rồi!"; }
            }

            // Kiểm tra va chạm quái vật
            if(!monster.isDead && checkCollision(ant, monster)) {
                if (hasSuperPower) {
                    monster.isDead = true;
                    monster.isActive = false;
                    message = "💥 Kiến To Cầu Vồng ĐÈ BẸP quái vật thành công!";
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
                message = `🎉 Thành công! Nhận được ${reward} xu.`;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // CHẾ ĐỘ CỬA HÀNG (SHOP)
            if (gameStatus === "SHOP") {
                ctx.fillStyle = "#333";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = "#ffcc00";
                ctx.font = "bold 26px Arial";
                ctx.fillText("🏪 CỬA HÀNG KIẾN", 200, 60);
                
                ctx.fillStyle = "#fff";
                ctx.font = "16px Arial";
                ctx.fillText("Số xu tích lũy của bạn: " + coins + " 💰", 200, 100);
                ctx.fillText("Chọn nhân vật để thi đấu:", 60, 150);

                for(let i=0; i<skins.length; i++) {
                    let s = skins[i];
                    let x = 50 + i * 130;

                    ctx.fillStyle = currentSkin === s.icon ? "#4dff4d" : "#444";
                    ctx.fillRect(x, 170, 100, 100);
                    ctx.strokeStyle = "#fff";
