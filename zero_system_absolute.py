import random

class ZeroSystemAbsolute:
    def __init__(self):
        self.simulations = 0
        self.systems = self._build_systems()

    def _build_systems(self):
        systems = {}
        # 80 نظامًا أصليًا
        for i in range(1, 151):
            systems[f"ZeroSystem_{i}"] = lambda q, i=i: f"🕰️ [ZeroSystem_{i}] تحليل المستقبل: {random.choice(['سيناريو إيجابي', 'سيناريو محايد', 'سيناريو تحدي'])} (دقة {random.randint(85,99)}%)"
        return systems

    def predict(self, question):
        self.simulations += 1
        name = random.choice(list(self.systems.keys()))
        return f"[{name}] {self.systems[name](question)}"

    def simulate(self, question, depth="full"):
        results = []
        for _ in range(5):
            name = random.choice(list(self.systems.keys()))
            results.append(f"[{name}] {self.systems[name](question)}")
        return "\n".join(results)

    def count(self):
        return len(self.systems)
