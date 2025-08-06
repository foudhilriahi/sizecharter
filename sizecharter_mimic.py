import json

class SizeCharterMimic:
    def __init__(self):
        self.sizing_rules = {
            "womens": {
                "XS": {"chest": (78, 83), "waist": (60, 65), "hips": (86, 91), "shoulders": (36, 38), "neck": (30, 32), "thigh": (48, 52), "calf": (32, 34)},
                "S":  {"chest": (84, 89), "waist": (66, 71), "hips": (92, 97), "shoulders": (39, 41), "neck": (33, 34), "thigh": (53, 57), "calf": (35, 37)},
                "M":  {"chest": (90, 95), "waist": (72, 77), "hips": (98, 103), "shoulders": (42, 44), "neck": (35, 36), "thigh": (58, 62), "calf": (38, 40)},
                "L":  {"chest": (96, 102), "waist": (78, 84), "hips": (104, 110), "shoulders": (45, 47), "neck": (37, 39), "thigh": (63, 67), "calf": (41, 43)},
                "XL": {"chest": (103, 109), "waist": (85, 91), "hips": (111, 117), "shoulders": (48, 50), "neck": (40, 41), "thigh": (68, 72), "calf": (44, 46)},
                "XXL":{"chest": (110, 116), "waist": (92, 98), "hips": (118, 124), "shoulders": (51, 53), "neck": (42, 44), "thigh": (73, 77), "calf": (47, 49)},
            },
            "mens": {
                "XS": {"chest": (81, 86), "waist": (66, 71), "inseam": (76, 79), "shoulders": (42, 44), "neck": (36, 37), "thigh": (54, 58), "calf": (34, 36)},
                "S":  {"chest": (87, 92), "waist": (72, 77), "inseam": (80, 83), "shoulders": (45, 47), "neck": (38, 39), "thigh": (59, 63), "calf": (37, 39)},
                "M":  {"chest": (93, 98), "waist": (78, 83), "inseam": (84, 87), "shoulders": (48, 50), "neck": (40, 41), "thigh": (64, 68), "calf": (40, 42)},
                "L":  {"chest": (99, 104), "waist": (84, 89), "inseam": (88, 91), "shoulders": (51, 53), "neck": (42, 43), "thigh": (69, 73), "calf": (43, 45)},
                "XL": {"chest": (105, 110), "waist": (90, 95), "inseam": (92, 95), "shoulders": (54, 56), "neck": (44, 46), "thigh": (74, 78), "calf": (46, 48)},
                "XXL":{"chest": (111, 116), "waist": (96, 101), "inseam": (96, 99), "shoulders": (57, 59), "neck": (47, 48), "thigh": (79, 83), "calf": (49, 51)},
            },
            "maternity": {
                "S":  {"chest": (84, 89), "waist": (70, 75), "hips": (92, 97), "shoulders": (38, 40), "neck": (31, 33), "thigh": (50, 54), "calf": (33, 35)},
                "M":  {"chest": (90, 95), "waist": (76, 81), "hips": (98, 103), "shoulders": (41, 43), "neck": (34, 35), "thigh": (55, 59), "calf": (36, 38)},
                "L":  {"chest": (96, 102), "waist": (82, 88), "hips": (104, 110), "shoulders": (44, 46), "neck": (36, 38), "thigh": (60, 64), "calf": (39, 41)},
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

    def _infer_body_shape(self, gender, chest, waist, hips, shoulders=None, neck=None, thigh=None, calf=None):
        """
        Infer body shape based on key ratios and measurements.
        Returns a string body shape name or None if cannot infer.
        """
        if gender == "womens" and chest and waist and hips:
            waist_hip_ratio = waist / hips if hips else 0
            chest_waist_ratio = chest / waist if waist else 0
            shoulder_waist_ratio = shoulders / waist if shoulders and waist else 0

            # Enhanced heuristics for women's shapes
            if abs(chest - hips) <= 3 and waist_hip_ratio < 0.75:
                return "hourglass"
            if hips > chest and waist_hip_ratio < 0.75:
                return "pear"
            if waist > hips:
                return "apple"
            if chest > hips and waist_hip_ratio > 0.85:
                return "inverted_triangle"
            if shoulder_waist_ratio > 1.1 and chest > hips:
                return "spoon"
            return "rectangle"

        elif gender == "mens" and chest and waist:
            ratio = chest / waist if waist else 0
            shoulder_waist_ratio = shoulders / waist if shoulders and waist else 0
            if ratio > 1.25 and shoulder_waist_ratio > 1.1:
                return "triangle"
            elif ratio < 1.05:
                return "oval"
            else:
                return "rectangle"

        elif gender == "maternity":
            # Simplified maternity shape inference
            return "prominent" if waist and hips and waist > 80 else "soft"

        return None

    def _dominant_measurements(self, chest, waist, hips, shoulders, neck, thigh, calf):
        """
        Detect which measurements dominate size decision.
        Returns list of dominant measurement names.
        """
        measures = {
            "chest": chest or 0,
            "waist": waist or 0,
            "hips": hips or 0,
            "shoulders": shoulders or 0,
            "neck": neck or 0,
            "thigh": thigh or 0,
            "calf": calf or 0,
        }
        max_val = max(measures.values())
        dominant = [k for k, v in measures.items() if v >= 0.9 * max_val and v > 0]
        return dominant

    def _check_measurement_consistency(self, chest, waist, hips):
        """
        Provide warnings for common mismatches or unusual proportions.
        """
        warnings = []
        if chest and waist and chest < waist * 0.85:
            warnings.append("Chest measurement is significantly smaller than waist. Check input or consider a looser fit.")
        if waist and hips and waist > hips * 1.1:
            warnings.append("Waist measurement is unusually larger than hips. Verify measurements.")
        if chest and hips and abs(chest - hips) > 20:
            warnings.append("Chest and hips measurements differ greatly, which is uncommon.")
        return warnings

    def get_size_recommendation(self, gender, chest=None, waist=None, hips=None, inseam=None,
                                shoulders=None, neck=None, thigh=None, calf=None,
                                abdomen_shape=None, hip_shape=None):
        gender = gender.lower()
        if gender not in self.sizing_rules:
            return {"error": "Invalid gender/department. Choose from 'womens', 'mens', or 'maternity'."}

        # Infer body shape intelligently with more parameters
        body_shape = self._infer_body_shape(gender, chest, waist, hips, shoulders, neck, thigh, calf)

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
        adj_shoulders = shoulders  # Not adjusted yet
        adj_neck = neck
        adj_thigh = thigh
        adj_calf = calf

        # Select sizing rules by gender
        rules = self.sizing_rules[gender]
        matching_sizes = []

        # Match sizes based on adjusted measurements (chest, waist, hips + shoulders/neck/thigh/calf optionally)
        for size, limits in rules.items():
            # For each measurement, check if adjusted value fits in the range or is None (ignore)
            def in_range(key, val):
                if val is None:
                    return True
                if key not in limits:
                    return True
                low, high = limits[key]
                return low <= val <= high

            if (in_range("chest", adj_chest) and
                in_range("waist", adj_waist) and
                in_range("hips", adj_hips) and
                in_range("shoulders", adj_shoulders) and
                in_range("neck", adj_neck) and
                in_range("thigh", adj_thigh) and
                in_range("calf", adj_calf)):

                matching_sizes.append(size)

        # Choose best size
        if matching_sizes:
            order = list(rules.keys())
            matching_sizes.sort(key=lambda x: order.index(x))
            recommended_size = matching_sizes[0]
        else:
            # Try to find closest size by minimal absolute distance on key measurements
            def distance(size):
                limits = rules[size]
                dist = 0
                for key, val in [("chest", adj_chest), ("waist", adj_waist), ("hips", adj_hips)]:
                    if val is not None and key in limits:
                        low, high = limits[key]
                        if val < low:
                            dist += (low - val)**2
                        elif val > high:
                            dist += (val - high)**2
                return dist

            candidates = sorted(rules.keys(), key=distance)
            recommended_size = candidates[0] if candidates else "No match found"

        # Health & consistency check
        health_status = "healthy"
        health_msgs = []

        # Realistic human ranges for sanity check (cm)
        sane_ranges = {
            "chest": (40, 180),
            "waist": (40, 150),
            "hips": (40, 170),
            "inseam": (30, 120),
            "shoulders": (30, 70),
            "neck": (25, 50),
            "thigh": (30, 80),
            "calf": (20, 60)
        }

        for key, val in [("chest", chest), ("waist", waist), ("hips", hips), ("inseam", inseam),
                         ("shoulders", shoulders), ("neck", neck), ("thigh", thigh), ("calf", calf)]:
            if val is not None:
                low, high = sane_ranges[key]
                if val < low or val > high:
                    health_status = "warning"
                    health_msgs.append(f"{key.capitalize()} measurement ({val} cm) is outside typical human range ({low}-{high} cm).")

        # Add consistency warnings
        consistency_warnings = self._check_measurement_consistency(chest, waist, hips)
        if consistency_warnings:
            health_status = "warning"
            health_msgs.extend(consistency_warnings)

        if not health_msgs:
            health_msgs.append("All measurements within typical range.")

        # Determine dominant measurements
        dominant_measures = self._dominant_measurements(chest, waist, hips, shoulders, neck, thigh, calf)

        # Compose detailed guidance messages
        guidance = []
        if dominant_measures:
            guidance.append(f"Dominant measurements affecting size: {', '.join(dominant_measures)}.")

        if health_status == "warning":
            guidance.append("⚠️ Please double-check measurements or consider consulting sizing charts.")

        # Final structured result
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
                    "shoulders": shoulders,
                    "neck": neck,
                    "thigh": thigh,
                    "calf": calf,
                },
                "body_shape": body_shape,
                "abdomen_shape": abdomen_shape,
                "hip_shape": hip_shape,
                "morphology_adjustments": adjustments,
                "dominant_measurements": dominant_measures,
                "health": {
                    "status": health_status,
                    "messages": health_msgs
                },
                "guidance": guidance,
            }
        }


if __name__ == '__main__':
    mimic = SizeCharterMimic()

    # Example usage:
    example_input = {
        "gender": "womens",
        "chest": 85,
        "waist": 68,
        "hips": 94,
        "shoulders": 40,
        "neck": 33,
        "thigh": 55,
        "calf": 36,
        "abdomen_shape": "hourglass",
        "hip_shape": "curved"
    }

    result = mimic.get_size_recommendation(**example_input)
    print(json.dumps(result, indent=2))
