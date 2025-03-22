// js/powerups.js
// Power-up system for Asteroids

class PowerUp {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.radius = 10;
        this.type = type; // 'shield', 'double-shot', etc.
        this.duration = 5000; // 5 seconds
        this.active = true;
    }

    draw(ctx) {
        if (!this.active) return;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.strokeStyle = this.type === 'shield' ? 'cyan' : 'orange';
        ctx.stroke();
        ctx.closePath();
    }

    update() {
        // Optionally animate or move power-up
    }

    applyEffect(player) {
        if (this.type === 'shield') {
            player.activateShield(this.duration);
        } else if (this.type === 'double-shot') {
            player.activateDoubleShot(this.duration);
        }
        this.active = false;
    }
}
