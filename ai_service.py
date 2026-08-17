try:
    import g4f

    def ask_gemini(prompt):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response
        except Exception as e:
            return f"⚠️ خطأ: {e}"
except ImportError:
    def ask_gemini(prompt):
        return "⚠️ مكتبة g4f غير مثبتة"
