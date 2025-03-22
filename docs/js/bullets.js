// js/bullet.js

class Bullet {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.speed = 5;
    }

    update() {
        this.y -= this.speed;
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = 'white';
        ctx.fill();
    }
}
