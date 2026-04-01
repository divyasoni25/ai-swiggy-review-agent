from agents.ingestion_agent import IngestionAgent
from agents.extraction_agent import ExtractionAgent
from agents.normalization_agent import NormalizationAgent
from agents.memory_agent import MemoryAgent
from agents.report_agent import ReportAgent
from sentence_transformers import SentenceTransformer
from datetime import datetime, timedelta
from agents.auto_taxonomy_agent import AutoTaxonomyDiscoveryAgent
import os

class ReviewTrendAgent:

    def __init__(self):
        self.ingestion = IngestionAgent()
        self.extractor = ExtractionAgent()
        self.normalizer = NormalizationAgent()
        self.memory = MemoryAgent()
        self.reporter = ReportAgent()
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.auto_taxonomy_agent = AutoTaxonomyDiscoveryAgent()
    def run(self, app_id, start_date, target_date):

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(target_date, "%Y-%m-%d")

        while start <= end:
            date_str = start.strftime("%Y-%m-%d")
            print(f"\nProcessing {date_str}")

            # 1️⃣ Fetch reviews
            reviews = self.ingestion.fetch_reviews(app_id, date_str)
            #print(f"Total reviews fetched: {len(reviews)}")
            #print("Sample review:", reviews[:2])

            if not reviews:
                start += timedelta(days=1)
                continue

            # Sample reviews
            reviews = reviews[:100]
            print(f"Reviews after sampling: {len(reviews)}")

            # Save raw
            self.ingestion.save_raw(reviews, date_str)

            # Extract topics
            topics, unmatched = self.extractor.extract_topics(reviews)
            print(f"Total extracted topics: {len(topics)}")

            # AUTO TAXONOMY DISCOVERY (ONLY on unmatched data)
            new_topics = self.auto_taxonomy_agent.discover_topics(unmatched)

            # Inject into extractor + normalizer
            for topic, keywords in new_topics.items():
                if topic not in self.extractor.taxonomy:
                    print(f"New topic discovered: {topic} - {keywords}")
                    self.extractor.taxonomy[topic] = keywords
                    self.normalizer.allowed_topics.add(topic)


            if not topics:
                start += timedelta(days=1)
                continue

            # Limit topics
            topics = topics[:20]
            print(f"Topics after limiting: {len(topics)}")

            # Fetch memory
            existing_topics = self.memory.get_topics()

            # Batch embeddings
            embeddings = self.embedder.encode(topics)

            for i, (topic, emb_vec) in enumerate(zip(topics, embeddings)):
                raw_topic = topic
                topic = self.normalizer.normalize_text(topic)

                if not self.normalizer.is_valid_topic(topic):
                    continue

                print(f"Processing topic {i+1}/{len(topics)} - RAW: {raw_topic} | NORMALIZED: {topic}")

                # Normalize text
                topic = self.normalizer.normalize_text(topic)

                # Skip junk
                if not self.normalizer.is_valid_topic(topic):
                    continue

                emb_blob = emb_vec.astype("float32").tobytes()

                # Deduplicate semantically
                canonical = self.normalizer.normalize_topic(
                    emb_blob, topic, existing_topics
                )

                # Store
                self.memory.save_topic(canonical, emb_blob)
                self.memory.increment_count(date_str, canonical)

            start += timedelta(days=1)

        # Generate report
        self.reporter.generate(target_date)


def ensure_directories():
    os.makedirs("data/raw_reviews", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("memory", exist_ok=True)
    os.makedirs("output", exist_ok=True)


if __name__ == "__main__":
    ensure_directories()

    agent = ReviewTrendAgent()
    agent.run(
        app_id="in.swiggy.android",
        start_date="2026-03-28",
        target_date="2026-04-1"
    )
