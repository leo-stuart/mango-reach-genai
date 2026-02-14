"""Entry point for the MangoAI API server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.presentation.api.main:app", host="0.0.0.0", port=8009, reload=True)
