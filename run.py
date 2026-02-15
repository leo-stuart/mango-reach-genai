"""Entry point for the MangoAI API server."""

import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8009))
    uvicorn.run("api.presentation.api.main:app", host="0.0.0.0", port=port)
