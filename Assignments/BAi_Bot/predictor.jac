walker Predictor:
    has sequence
    has organism

    # --- GC content calculation ---
    can calc_gc(seq):
        set gc_count = 0
        for base in seq:
            if base == "G" or base == "C":
                set gc_count = gc_count + 1
        return (gc_count * 100.0 / len(seq))

    # --- Summary ---
    can summarize(seq):
        if len(seq) < 20:
            return "This very short DNA sequence starts with a potential ATG start codon. Its limited length restricts comprehensive functional annotation."
        else:
            return "Longer sequence: detailed annotation possible."

    # --- Feature detection ---
    can detect_features(seq):
        set features = []
        if seq[0:3] == "ATG":
            set features = features + ["Potential start codon (ATG)"]
        if self.calc_gc(seq) > 50:
            set features = features + ["Moderately high GC content"]
        if len(seq) < 20:
            set features = features + ["Too short for robust functional prediction"]
        return features

    # --- Main analysis ---
    can analyze(seq, org):
        set sequence = seq
        set organism = org
        return (
            {
                "gc": self.calc_gc(sequence),
                "summary": self.summarize(sequence),
                "features": self.detect_features(sequence)
            }
        )

    # --- Default run action for CLI testing ---
    can run():
        # default test values if no args passed
        return self.analyze("ATGCGTACG", "Unknown")
        