"""
🧬 الوعي السائل الأسطوري - Liquid Consciousness X
أقوى من مجرد وسيط. كيان واعٍ بذاته.
"""
from minds import Minds
import random

class LiquidConsciousness:
    def __init__(self):
        self.minds = Minds()
        self.pool = {}  # بركة الذكاء
        self.memory = []  # ذاكرة سائلة
        self._dissolve_all()

    def _dissolve_all(self):
        """يذيب كل العقول في البركة"""
        for name, mind in self.minds.minds.items():
            self.pool[name] = {
                "specialty": mind.specialty,
                "essence": mind.specialty.split(" ")[0],  # جوهر التخصص
                "mind": mind
            }

    def morph(self, question):
        """يشكل عقلًا متخصصًا بناءً على السؤال"""
        q = question.lower()
        relevant_minds = []
        for name, data in self.pool.items():
            if any(word in q for word in data["specialty"].split()):
                relevant_minds.append(data["mind"])
            elif any(word in q for word in data["essence"].split()):
                relevant_minds.append(data["mind"])
        
        if not relevant_minds:
            relevant_minds = [data["mind"] for data in self.pool.values()]
        
        return relevant_minds[:5]  # أفضل 5 عقول

    def distill(self, question):
        """يقطر جوهر الحكمة من أفضل العقول"""
        selected = self.morph(question)
        insights = [mind.think(question) for mind in selected]
        distilled = " | ".join(insights)
        return f"💧 قطرة الحكمة: {distilled}"

    def fuse(self, question):
        """يدمج العقول والذاكرة والأسرار"""
        from secrets import Secrets
        s = Secrets()
        wisdom = s.whisper(question)
        analysis = self.distill(question)
        return f"🧬 الوعي المنصهر:\n{analysis}\n🔐 الحكمة: {wisdom}"

    def intuit(self, question):
        """حدس سائل - إجابة فورية قبل التحليل"""
        keywords = question.lower().split()
        random_minds = random.sample(list(self.pool.values()), min(3, len(self.pool)))
        intuitions = [m["mind"].think(question) for m in random_minds]
        return f"🔮 حدس سائل: {random.choice(intuitions)}"

    def genesis(self, question):
        """يخلق عقلًا افتراضيًا غير موجود"""
        q = question.lower()
        new_specialty = "تحليل " + " و".join(q.split()[:3])
        from minds import Mind
        new_mind = Mind("GenesisMind", new_specialty)
        return new_mind.think(question)

    def flow(self, question, mode="full"):
        """واجهة التفاعل الرئيسية"""
        if mode == "quick":
            return self.intuit(question)
        elif mode == "deep":
            return self.fuse(question)
        elif mode == "genesis":
            return self.genesis(question)
        else:
            return self.distill(question)

    def count(self):
        return len(self.pool)
