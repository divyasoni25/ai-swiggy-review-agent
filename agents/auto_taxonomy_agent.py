# agents/auto_taxonomy_agent.py
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

class AutoTaxonomyDiscoveryAgent:
    def __init__(self, min_cluster_size=3):
        self.min_cluster_size = min_cluster_size
        self.new_topics = {}

        # Sentiment / junk to ignore
        self.junk_tokens = {
            "good", "nice", "very good", "awesome", "amazing",
            "best", "ok", "okay", "super", "bhai", "thanks", "thnks",
            "love", "great", "excellent", "grateful", "mast"
        }

    def clean_text(self, text):
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def is_junk(self, text):
        return text in self.junk_tokens or len(text.split()) < 2

    def discover_topics(self, unmatched_phrases):
        """
        Input: list of unmatched review texts
        Output: dict of new_topic → keyword list
        """

        if len(unmatched_phrases) < self.min_cluster_size:
            return {}

        # 🔍 Clean + filter junk
        cleaned = []
        for t in unmatched_phrases:
            c = self.clean_text(t)
            if c and not self.is_junk(c):
                cleaned.append(c)

        # 🛑 If still too small, skip discovery
        if len(cleaned) < self.min_cluster_size:
            return {}

        # ⚠️ TF-IDF with safe parameters
        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 3),
                min_df=1   # <-- FIX: was 2, which caused empty vocab
            )
            X = vectorizer.fit_transform(cleaned)
        except ValueError:
            # Graceful exit if vocabulary is empty
            return {}

        # 🧠 Cluster
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1.2
        )
        labels = clustering.fit_predict(X.toarray())

        clusters = {}
        for text, label in zip(cleaned, labels):
            clusters.setdefault(label, []).append(text)

        discovered = {}

        for cluster_texts in clusters.values():
            if len(cluster_texts) < self.min_cluster_size:
                continue

            topic_name, keywords = self._name_cluster(cluster_texts)
            if topic_name:
                discovered[topic_name] = keywords

        self.new_topics = discovered
        return discovered

    def _name_cluster(self, texts):
        """
        Create a topic name from cluster using keyword frequency.
        """
        try:
            tfidf = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                min_df=1
            )
            X = tfidf.fit_transform(texts)
        except ValueError:
            return None, None

        terms = tfidf.get_feature_names_out()
        scores = X.sum(axis=0).A1
        ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)

        top_keywords = [kw for kw, _ in ranked[:5]]
        joined = " ".join(top_keywords)

        # Heuristic naming rules
        if "refund" in joined:
            return "refund issue", top_keywords
        if "cancel" in joined:
            return "order cancellation issue", top_keywords
        if "rude" in joined or "behavior" in joined:
            return "delivery partner rude", top_keywords
        if "map" in joined or "location" in joined:
            return "maps not working", top_keywords
        if "feature" in joined or "should" in joined:
            return "feature request", top_keywords

        # Fallback only if meaningful
        if len(top_keywords[0].split()) >= 2:
            return top_keywords[0], top_keywords

        return None, None
