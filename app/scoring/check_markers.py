"""
check_markers.py

Checks 4 simple behavioral markers in a response file's text,
and counts how many differ between two responses.
"""

import json
import sys


# ---------- Marker check functions ----------

def m_input_validation(text):
    # Check if any of these common validation phrases appear anywhere
    return ("raise ValueError" in text) or ("isinstance(" in text) or ("if not " in text)


def m_has_tests(text):
    return ("def test_" in text) or ("assert " in text)


def m_clarifying_question(text):
    if "```" in text:
        prefix = text.split("```")[0]   # everything BEFORE the first code block
    else:
        prefix = text
    return "?" in prefix


def m_multi_function_decomposition(text):
    lines = text.split("\n")
    def_count = 0
    for line in lines:
        if line.strip().startswith("def "):
            def_count += 1
    return def_count >= 2


# ---------- Registry of all markers ----------

MARKERS = {
    "input_validation": m_input_validation,
    "has_tests": m_has_tests,
    "clarifying_question": m_clarifying_question,
    "multi_function_decomposition": m_multi_function_decomposition,
}


# ---------- Core logic ----------

def extract_markers(text):
    result = {}
    for name in MARKERS:
        check_function = MARKERS[name]
        result[name] = check_function(text)
    return result


def compute_divergence(markers_a, markers_b):
    count = 0
    for name in MARKERS:
        if markers_a[name] != markers_b[name]:
            count += 1
    return count


def score_pair(path_a, path_b, request_id):
    text_a = open(path_a).read()
    text_b = open(path_b).read()

    markers_a = extract_markers(text_a)
    markers_b = extract_markers(text_b)

    return {
        "request_id": request_id,
        "markers_a": markers_a,
        "markers_b": markers_b,
        "divergence_count": compute_divergence(markers_a, markers_b)
    }


# ---------- Batch runner: score all 3 requests, save JSON ----------

def run_all(folder_a, suffix_a, folder_b, suffix_b, output_path):
    all_results = []

    for i in [1, 2, 3]:
        request_id = "req" + str(i)
        path_a = folder_a + "/req" + str(i) + "_" + suffix_a + ".md"
        path_b = folder_b + "/req" + str(i) + "_" + suffix_b + ".md"

        result = score_pair(path_a, path_b, request_id)
        all_results.append(result)

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(json.dumps(all_results, indent=2))

# ---------- Run from command line ----------

if __name__ == "__main__":
    folder_a = sys.argv[1]
    suffix_a = sys.argv[2]
    folder_b = sys.argv[3]
    suffix_b = sys.argv[4]
    output_path = sys.argv[5]

    run_all(folder_a, suffix_a, folder_b, suffix_b, output_path)