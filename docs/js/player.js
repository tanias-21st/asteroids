// js/player.js
// Extending player ship with power-up abilities

class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 20;
        this.shieldActive = false;
        this.doubleShotActive = false;
        this.shieldTimer = 0;
        this.doubleShotTimer = 0;
    }

    activateShield(duration) {
        this.shieldActive = true;
        this.shieldTimer = Date.now() + duration;
    }

    activateDoubleShot(duration) {
        this.doubleShotActive = true;
        this.doubleShotTimer = Date.now() + duration;
    }

    update() {
        // Deactivate shield after timer expires
        if (this.shieldActive && Date.now() > this.shieldTimer) {
            this.shieldActive = false;
        }

        // Deactivate double-shot after timer expires
        if (this.doubleShotActive && Date.now() > this.doubleShotTimer) {
            this.doubleShotActive = false;
        }

        // Normal player movement and other updates...
    }

    draw(ctx) {
        // Ship shape
        ctx.beginPath();
        ctx.moveTo(this.x, this.y - 20);
        ctx.lineTo(this.x - 15, this.y + 15);
        ctx.lineTo(this.x + 15, this.y + 15);
        ctx.closePath();
        ctx.strokeStyle = 'white';
        ctx.stroke();

        // Optional: Shield glow
        if (this.shieldActive) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius + 5, 0, Math.PI * 2);
            ctx.strokeStyle = 'cyan';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.lineWidth = 1;
        }
    }

    shoot(bullets) {
        if (this.doubleShotActive) {
            bullets.push(new Bullet(this.x - 5, this.y - 20));
            bullets.push(new Bullet(this.x + 5, this.y - 20));
        } else {
            bullets.push(new Bullet(this.x, this.y - 20));
        }
    }
}
