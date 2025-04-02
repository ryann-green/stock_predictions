from apig_wsgi import make_lambda_handler
from app import server

lambda_handler = make_lambda_handler(server)

# For local Dash development
if __name__ == "__main__":
    import os
    if os.getenv("LOCAL_DEV") == "true":
        print("🔧 Running locally at http://0.0.0.0:8050")
        server.run(debug=True, host="0.0.0.0", port=8050)
