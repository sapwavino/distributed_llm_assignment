import express from 'express';
import apiRoutes from './routes/api';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use('/api', apiRoutes);

app.listen(PORT, () => {
    console.log(`Node.js API server running on port ${PORT}`);
});