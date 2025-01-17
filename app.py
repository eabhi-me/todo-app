# importing the app form directory app
from app import app

# running the development server
if __name__ == '__main__':
    app.run(debug=True)


# deployment server
# import os
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)