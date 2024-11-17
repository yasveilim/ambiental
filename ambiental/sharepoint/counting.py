import typing as t


class StatisticsControlller:
    def __init__(self):
        self._counts = {"na": 0, "delivered": 0, "pending": 0}
        self._statistics = {}

    def  analize_materials(self, all_materials: t.Dict[str, dict]):
        for material in all_materials:
            material_data = all_materials[material]
            
            for category in material_data:
                self.count_advance(material_data[category], material)
    

    def count_advance(self, books_list: t.List[dict], tag: str):
        if tag not in self._statistics:
            self._statistics[tag] = self._counts.copy()

        for item in books_list:
            has_advance = item.get("advance")
            if has_advance != None and has_advance.lower() in self._counts:
                self._statistics[tag][has_advance.lower()] += 1

    def apply_analytics(self):
        for tag, counts in self._statistics.items():
            total_required = counts["delivered"] + counts["pending"] + counts["na"]
            applicable_requirements = total_required - counts["na"]
            total = (counts["delivered"] / total_required) * 100 if total_required > 0 else 0

            self._statistics[tag].update({
                "total_required": total_required,
                "applicable_requirements": applicable_requirements,
                "total": f"{total:.2f}%",
            })

    def get_statistics(self):
        return self._statistics


def analyze_materials(all_materials: t.Dict[str, dict]):
    controller = StatisticsControlller()
    controller.analize_materials(all_materials)
    controller.apply_analytics()
    return controller.get_statistics()