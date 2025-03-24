function qualifiesForHighScore(score) {
    if (highScores.length < maxHighScores) return true;
    return score > highScores[highScores.length - 1].score;
}

function update() {
    if (!ship.alive) return;

    // Ship movement
    ship.x += ship.velX;
    ship.y += ship.velY;
    ship.velX *= ship.friction;
    ship.velY *= ship.friction;

    if (ship.x < 0) ship.x = canvas.width;
    if (ship.x > canvas.width) ship.x = 0;
    if (ship.y < 0) ship.y = canvas.height;
    if (ship.y > canvas.height) ship.y = 0;

    // Thruster particles
    if (Math.abs(ship.velX) > 0.02 || Math.abs(ship.velY) > 0.02) {
        particles.push({
            x: ship.x - Math.cos(ship.angle) * 15,
            y: ship.y - Math.sin(ship.angle) * 15,
            velX: (Math.random() - 0.5) * 0.5,
            velY: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 3 + 1,
            life: 1.0
        });
    }

    // Particles update
    particles.forEach((p, i) => {
        p.x += p.velX;
        p.y += p.velY;
        p.life -= 0.05;
        if (p.life <= 0) particles.splice(i, 1);
    });

    // Bullets
    bullets.forEach((b, i) => {
        b.x += b.velX;
        b.y += b.velY;
        if (b.x < 0 || b.x > canvas.width || b.y < 0 || b.y > canvas.height) {
            bullets.splice(i, 1);
        }
    });

    // Asteroids
    asteroids.forEach((a, i) => {
        a.x += a.speedX;
        a.y += a.speedY;
        if (a.x < 0) a.x = canvas.width;
        if (a.x > canvas.width) a.x = 0;
        if (a.y < 0) a.y = canvas.height;
        if (a.y > canvas.height) a.y = 0;

        // Asteroid vs Ship
        let dx = ship.x - a.x;
        let dy = ship.y - a.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < a.size / 2 + ship.size / 2) {
            if (activePowerUp !== "shield") {
                createExplosion(ship.x, ship.y, 50);
                ship.alive = false;
                gameOver = true;

                // Check for high score entry here:
                if (qualifiesForHighScore(score)) {
                    enteringInitials = true;
                    currentInitials = "";
                }
            }
        }

        // Asteroid vs Bullet
        bullets.forEach((b, j) => {
            let dx = b.x - a.x;
            let dy = b.y - a.y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < a.size / 2) {
                createExplosion(a.x, a.y, a.size);
                spawnPowerUp(a.x, a.y);
                bullets.splice(j, 1);
                asteroids.splice(i, 1);
                if (a.size > 30) {
                    let newSize = a.size / 2;
                    createAsteroids(2, a.x, a.y, newSize);
                }
            }
        });
    });

    // Explosions
    explosions.forEach((e, i) => {
        e.x += e.velX;
        e.y += e.velY;
        e.life -= 0.05;
        if (e.life <= 0) explosions.splice(i, 1);
    });

    // Power-up timer
    if (powerUpTimer > 0) {
        powerUpTimer--;
        if (powerUpTimer <= 0) activePowerUp = null;
    }

    // Level progression check
    if (asteroids.length === 0 && !gameOver) {
        if (level < maxLevel) {
            level++;
            startLevel();
        } else {
            // WIN CONDITION
            gameOver = true;
        }
    }
}
