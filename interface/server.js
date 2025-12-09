const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { router: authRoutes, verificarToken } = require('./auth');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));
app.use('/auth', authRoutes);
app.use("/api", verificarToken);


const sensores = {
    temp: { inicio: 5101, qtd: 4 },
    luz:  { inicio: 5201, qtd: 4 },
    ar:   { inicio: 5301, qtd: 4 }
};

for (const [tipo, conf] of Object.entries(sensores)) {
    for (let i = 1; i <= conf.qtd; i++) {

        const port = conf.inicio + (i - 1);
        const path = `/api/sensor/${tipo}${i}`;

        app.use(path, createProxyMiddleware({
            target: `http://localhost:${port}`,
            changeOrigin: true,
            pathRewrite: { '^/api/sensor': '/sensor' }
        }));

        console.log(`↳ Registrado proxy: ${path} → http://localhost:${port}`);
    }
}

app.use('/api/local', createProxyMiddleware({
    target: 'http://sensor_nivell:5000',
    changeOrigin: true,
    pathRewrite: { '^/api/sensor_local': '/local' }
}));

app.use('/api/historico', createProxyMiddleware({
    target: 'http://consulta_banco:5000',
    changeOrigin: true,
    pathRewrite: { '^/api/historico': '/get_sensor_data' }
}));

app.use('/api/historicor', createProxyMiddleware({
    target: 'http://consulta_bancor:5002',
    changeOrigin: true,
    pathRewrite: { '^/api/historicor': '/get_real_data' }
}));

app.use('/api/sensor_real', createProxyMiddleware({
    target: 'http://sensor_nivelr:5001',
    changeOrigin: true,
    pathRewrite: { '^/api/sensor_real': '/dados' }
}));

const PORT = 80;
app.listen(PORT, () => {
    console.log(`Interface rodando em http://localhost:${PORT}`);
});
