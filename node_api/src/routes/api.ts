import express, { Request, Response } from "express";
import axios from "axios";

const router = express.Router();
const PYTHON_API_URL = "http://python_api:5000"  // Docker service name 

// Endpoint to send a query to the Python model
router.post("/query", async (req: Request, res: Response) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: "Query cannot be empty." });
  }

  try {
    const response = await axios.post(`${PYTHON_API_URL}/query`, { query });
    res.json(response.data);
  } catch (error) {
    console.error("Error querying Python API:", error);
    if (axios.isAxiosError(error)) {
      return res.status(error.response?.status || 500).json({
        error:
          error.response?.data?.error ||
          "An error occurred while contacting the Python API."
      });
    }
    return res.status(500).json({ error: "An unexpected error occurred." });
  }
});


router.get("/history", async (req: Request, res: Response) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/history`);
    res.json(response.data);
  } catch (error) {
    console.error("Error fetching history:", error);
    if (axios.isAxiosError(error)) {
      return res.status(error.response?.status || 500).json({
        error:
          error.response?.data?.error ||
          "An error occurred while fetching history."
      });
    }
    return res.status(500).json({ error: "An unexpected error occurred." });
  }
});

router.get("/conversation/<conversation_id>", async (req: Request, res: Response, ) => {
  const { conversation_id } = req.params;
  try {
    const response = await axios.get(`${PYTHON_API_URL}/conversation/${conversation_id}`);
    res.json(response.data);
  } catch (error) {
    console.error("Error fetching history:", error);
    if (axios.isAxiosError(error)) {
      return res.status(error.response?.status || 500).json({
        error:
          error.response?.data?.error ||
          "An error occurred while fetching history."
      });
    }
    return res.status(500).json({ error: "An unexpected error occurred." });
  }
});

export default router;
