from app import create_app

app = create_app()

if __name__ == "__main__":
    # Apenas para debug/local
    app.run(host="0.0.0.0", port=8000, debug=True)
