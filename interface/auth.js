const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const router = express.Router();

const SECRET = "MINHA_CHAVE_SECRETA_123";

// 🧍 Usuários de exemplo (depois pode estar no banco)
const users = [
    { username: "admin", password: bcrypt.hashSync("123456", 10) },
    { username: "mvv", password: bcrypt.hashSync("senha2003", 10) }
];

// LOGIN
router.post('/login', (req, res) => {
    const { username, password } = req.body;

    const user = users.find(u => u.username === username);
    if (!user) return res.status(401).json({ msg: "Usuário não encontrado" });

    if (!bcrypt.compareSync(password, user.password))
        return res.status(403).json({ msg: "Senha incorreta" });

    const token = jwt.sign({ username }, SECRET, { expiresIn: '8h' });

    res.json({ token, username });
});

function verificarToken(req, res, next) {
    const token = req.headers.authorization?.split(" ")[1];

    if (!token) return res.status(401).json({ msg: "Token ausente" });

    jwt.verify(token, SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ msg: "Token inválido" });

        req.user = decoded;
        next();
    });
}
module.exports = { router, verificarToken };