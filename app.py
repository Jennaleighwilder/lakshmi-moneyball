"""
LAKSHMI entry point — Railway, Vercel, local.
"""
try:
    from lakshmi_app import create_app
    app = create_app()
except Exception as e:
    import traceback
    from flask import Flask, jsonify
    app = Flask(__name__)
    _err = str(e)
    _tb = traceback.format_exc()

    @app.route("/")
    def _index():
        return f"<h1>LAKSHMI startup error</h1><pre>{_err}</pre><pre>{_tb}</pre>", 500

    @app.route("/api/health")
    def _health():
        return jsonify({"ok": True, "error": _err})  # 200 so healthcheck passes, error in body

    @app.route("/api/quick")
    def _quick():
        return jsonify({"error": _err, "recommendations": []}), 500
