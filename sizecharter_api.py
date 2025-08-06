from flask import Flask, request, jsonify
from flask_cors import CORS

class SizeCharterTuned:
    def __init__(self):
        # Size charts now include new fields: shoulders, neck, thigh, calf (example ranges)
        self.sizing_rules = {
            "womens": {
                "XS": {"chest": (78, 83), "waist": (60, 65), "hips": (86, 91), "shoulders": (35, 38), "neck": (30, 33), "thigh": (45, 50), "calf": (30, 35)},
                "S":  {"chest": (84, 89), "waist": (66, 71), "hips": (92, 97), "shoulders": (39, 41), "neck": (34, 36), "thigh": (51, 56), "calf": (36, 40)},
                "M":  {"chest": (90, 95), "waist": (72, 77), "hips": (98, 103), "shoulders": (42, 44), "neck": (37, 39), "thigh": (57, 62), "calf": (41, 45)},
                "L":  {"chest": (96, 102), "waist": (78, 84), "hips": (104, 110), "shoulders": (45, 47), "neck": (40, 42), "thigh": (63, 68), "calf": (46, 50)},
                "XL": {"chest": (103, 109), "waist": (85, 91), "hips": (111, 117), "shoulders": (48, 50), "neck": (43, 45), "thigh": (69, 74), "calf": (51, 55)},
                "XXL":{"chest": (110, 116), "waist": (92, 98), "hips": (118, 124), "shoulders": (51, 53), "neck": (46, 48), "thigh": (75, 80), "calf": (56, 60)},
            },
            "mens": {
                "XS": {"chest": (81, 86), "waist": (66, 71), "inseam": (76, 79), "shoulders": (40, 43), "neck": (35, 37), "thigh": (50, 55), "calf": (35, 38)},
                "S":  {"chest": (87, 92), "waist": (72, 77), "inseam": (80, 83), "shoulders": (44, 46), "neck": (38, 40), "thigh": (56, 61), "calf": (39, 43)},
                "M":  {"chest": (93, 98), "waist": (78, 83), "inseam": (84, 87), "shoulders": (47, 49), "neck": (41, 43), "thigh": (62, 67), "calf": (44, 48)},
                "L":  {"chest": (99, 104), "waist": (84, 89), "inseam": (88, 91), "shoulders": (50, 52), "neck": (44, 46), "thigh": (68, 73), "calf": (49, 53)},
                "XL": {"chest": (105, 110), "waist": (90, 95), "inseam": (92, 95), "shoulders": (53, 55), "neck": (47, 49), "thigh": (74, 79), "calf": (54, 58)},
                "XXL":{"chest": (111, 116), "waist": (96, 101), "inseam": (96, 99), "shoulders": (56, 58), "neck": (50, 52), "thigh": (80, 85), "calf": (59, 63)},
            },
            "maternity": {
                "S":  {"chest": (84, 89), "waist": (70, 75), "hips": (92, 97), "shoulders": (38, 41), "neck": (32, 34), "thigh": (47, 52), "calf": (31, 36)},
                "M":  {"chest": (90, 95), "waist": (76, 81), "hips": (98, 103), "shoulders": (42, 44), "neck": (35, 37), "thigh": (53, 58), "calf": (37, 41)},
                "L":  {"chest": (96, 102), "waist": (82, 88), "hips": (104, 110), "shoulders": (45, 47), "neck": (38, 40), "thigh": (59, 64), "calf": (42, 46)},
            }
        }

        self.morphology_adjustments = {
            "womens": {
                "hourglass": {"hips": +2, "waist": -1},
                "pear": {"hips": +3, "waist": 0},
                "apple": {"waist": +3, "hips": -1},
                "rectangle": {"waist": +1, "hips": 0},
                "inverted_triangle": {"chest": +2, "waist": 0},
                "spoon": {"hips": +3, "waist": +1},
                "diamond": {"waist": +2, "hips": 0}
            },
            "mens": {
                "triangle": {"chest": +2, "waist": -1},
                "rectangle": {},
                "inverted_triangle": {"chest": +2},
                "oval": {"waist": +3},
                "trapezoid": {}
            },
            "maternity": {
                "prominent": {"waist": +4, "hips": +1},
                "soft": {"waist": +2},
                "flat": {}
            }
        }

    def _infer_body_shape(self, gender, chest, waist, hips):
        """
        Infer body shape based on key ratios and measurements.
        Returns a string body shape name or None if cannot infer.
        """
        if gender == "womens" and chest and waist and hips:
            waist_hip_ratio = waist / hips if hips else 0
            chest_waist_ratio = chest / waist if waist else 0
            # Basic heuristics for women's shapes:
            if abs(chest - hips) <= 3 and waist_hip_ratio < 0.75:
                return "hourglass"
            if hips > chest and waist_hip_ratio < 0.75:
                return "pear"
            if waist > hips:
                return "apple"
            if chest > hips and waist_hip_ratio > 0.85:
                return "inverted_triangle"
            return "rectangle"
        
        elif gender == "mens" and chest and waist:
            ratio = chest / waist if waist else 0
            if ratio > 1.25:
                return "triangle"
            elif ratio < 1.05:
                return "oval"
            else:
                return "rectangle"
        
        elif gender == "maternity":
            # Maternity shapes inferred differently, but simplified here
            return "prominent" if waist and hips and waist > 80 else "soft"

        return None

    def get_size_recommendation(self, gender, chest=None, waist=None, hips=None, inseam=None,
                                shoulders=None, neck=None, thigh=None, calf=None,
                                abdomen_shape=None, hip_shape=None):
        gender = gender.lower()
        if gender not in self.sizing_rules:
            return {"error": "Invalid gender/department. Choose from 'womens', 'mens', or 'maternity'."}

        # Infer body shape
        body_shape = self._infer_body_shape(gender, chest, waist, hips)

        # Compose adjustments from morphology (body_shape + abdomen_shape + hip_shape)
        adjustments = {}
        for morph in [body_shape, abdomen_shape, hip_shape]:
            if morph and morph in self.morphology_adjustments.get(gender, {}):
                for key, val in self.morphology_adjustments[gender][morph].items():
                    adjustments[key] = adjustments.get(key, 0) + val

        # Apply adjustments to measurements
        adj_chest = chest + adjustments.get("chest", 0) if chest is not None else None
        adj_waist = waist + adjustments.get("waist", 0) if waist is not None else None
        adj_hips = hips + adjustments.get("hips", 0) if hips is not None else None
        adj_shoulders = shoulders  # no adjustments for new fields yet
        adj_neck = neck
        adj_thigh = thigh
        adj_calf = calf

        rules = self.sizing_rules[gender]

        # For each measurement field, get the smallest matching size (or None if no match)
        def get_size_for_measurement(name, value):
            if value is None:
                return None
            matching_sizes = []
            for size, limits in rules.items():
                if name not in limits:
                    continue
                low, high = limits[name]
                if low <= value <= high:
                    matching_sizes.append(size)
            if not matching_sizes:
                return None
            order = list(rules.keys())
            matching_sizes.sort(key=lambda x: order.index(x))
            return matching_sizes[0]

        # Get sizes from each measurement
        sizes = {}
        sizes['chest'] = get_size_for_measurement("chest", adj_chest)
        sizes['waist'] = get_size_for_measurement("waist", adj_waist)
        if gender != "mens":  # mens use inseam, womens and maternity use hips
            sizes['hips'] = get_size_for_measurement("hips", adj_hips)
        else:
            sizes['hips'] = None
        sizes['inseam'] = get_size_for_measurement("inseam", inseam)
        sizes['shoulders'] = get_size_for_measurement("shoulders", adj_shoulders)
        sizes['neck'] = get_size_for_measurement("neck", adj_neck)
        sizes['thigh'] = get_size_for_measurement("thigh", adj_thigh)
        sizes['calf'] = get_size_for_measurement("calf", adj_calf)

        # Find dominant size as max index of any measurement size (larger sizes mean bigger index)
        order = list(rules.keys())
        size_indices = []
        for key, size_val in sizes.items():
            if size_val in order:
                size_indices.append(order.index(size_val))
        if size_indices:
            dominant_index = max(size_indices)
            recommended_size = order[dominant_index]
        else:
            recommended_size = "No exact match found"

        # Build mismatch warnings if big differences between chest, waist, hips
        warnings = []
        if adj_chest is not None and adj_waist is not None:
            if adj_chest < 0.7 * adj_waist:
                warnings.append("Chest measurement is significantly smaller than waist; consider fit options.")
            elif adj_chest > 1.3 * adj_waist:
                warnings.append("Chest measurement is significantly larger than waist; consider fit options.")
        if adj_waist is not None and adj_hips is not None:
            if adj_waist > 1.3 * adj_hips:
                warnings.append("Waist measurement is significantly larger than hips; consider fit options.")
            elif adj_waist < 0.7 * adj_hips:
                warnings.append("Waist measurement is significantly smaller than hips; consider fit options.")

        # Health info
        health_status = "healthy"
        health_messages = []
        for key, val in [("chest", chest), ("waist", waist), ("hips", hips), ("inseam", inseam), ("shoulders", shoulders), ("neck", neck), ("thigh", thigh), ("calf", calf)]:
            if val is None:
                continue
            if val < 30 or val > 180:
                health_status = "warning"
                health_messages.append(f"{key.capitalize()} measurement is unusually low or high.")

        if not health_messages:
            health_messages.append("All measurements within typical range.")

        return {
            "recommended_size": recommended_size,
            "details": {
                "gender": gender,
                "original_measurements": {
                    "chest": chest,
                    "waist": waist,
                    "hips": hips,
                    "inseam": inseam,
                    "shoulders": shoulders,
                    "neck": neck,
                    "thigh": thigh,
                    "calf": calf,
                },
                "adjusted_measurements": {
                    "chest": round(adj_chest, 1) if adj_chest is not None else None,
                    "waist": round(adj_waist, 1) if adj_waist is not None else None,
                    "hips": round(adj_hips, 1) if adj_hips is not None else None,
                    "inseam": inseam,
                    "shoulders": adj_shoulders,
                    "neck": adj_neck,
                    "thigh": adj_thigh,
                    "calf": adj_calf,
                },
                "body_shape": body_shape,
                "abdomen_shape": abdomen_shape,
                "hip_shape": hip_shape,
                "morphology_adjustments": adjustments,
                "warnings": warnings,
                "health": {
                    "status": health_status,
                    "messages": health_messages
                }
            }
        }


app = Flask(__name__)
CORS(app)
sizer = SizeCharterTuned()

@app.route('/api/size', methods=['POST'])
def api_size():
    data = request.get_json(force=True)
    gender = data.get("gender")
    chest = data.get("chest")
    waist = data.get("waist")
    hips = data.get("hips")
    inseam = data.get("inseam")
    shoulders = data.get("shoulders")
    neck = data.get("neck")
    thigh = data.get("thigh")
    calf = data.get("calf")
    abdomen_shape = data.get("abdomen_shape")
    hip_shape = data.get("hip_shape")

    # Validate numeric fields
    def to_float_or_none(val):
        if val is None or val == '':
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    chest = to_float_or_none(chest)
    waist = to_float_or_none(waist)
    hips = to_float_or_none(hips)
    inseam = to_float_or_none(inseam)
    shoulders = to_float_or_none(shoulders)
    neck = to_float_or_none(neck)
    thigh = to_float_or_none(thigh)
    calf = to_float_or_none(calf)

    if not gender:
        return jsonify({"error": "Gender is required"}), 400

    result = sizer.get_size_recommendation(
        gender=gender,
        chest=chest,
        waist=waist,
        hips=hips,
        inseam=inseam,
        shoulders=shoulders,
        neck=neck,
        thigh=thigh,
        calf=calf,
        abdomen_shape=abdomen_shape,
        hip_shape=hip_shape
    )
    return jsonify(result)


if __name__ == "__main__":
    print("Starting SizeCharterTuned API on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
