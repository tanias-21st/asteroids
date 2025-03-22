// js/game.js

let powerUps = [];

function spawnPowerUp() {
    if (Math.random() < 0.01) { // ~1% chance per frame
        let x = Math.random() * canvas.width;
        let y = Math.random() * canvas.height;
        let type = Math.random() < 0.5 ? 'shield' : 'double-shot';
        powerUps.push(new PowerUp(x, y, type));
    }
}

function checkPowerUpCollision(player) {
    powerUps.forEach((powerUp, index) => {
        const dx = powerUp.x - player.x;
        const dy = powerUp.y - player.y;
        if (Math.sqrt(dx * dx + dy * dy) < player.radius + powerUp.radius) {
            powerUp.applyEffect(player);
            powerUps.splice(index, 1);
        }
    });
}

// Inside your game loop:
spawnPowerUp();
powerUps.forEach(pu => {
    pu.update();
    pu.draw(ctx);
});
checkPowerUpCollision(player);
