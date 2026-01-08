from google_play_scraper import reviews, Sort
from datetime import datetime
from collections import defaultdict
import os
import pandas as pd


class IngestionAgent:
    def __init__(self):
        self.cached_reviews_by_date = None

    # INTERNAL: FETCH RECENT REVIEWS
    def _fetch_recent_reviews(self, app_id, max_pages=20):
        """
        Fetches the most recent reviews from Google Play and returns
        a list of dicts: {"text": ..., "date": ...}
        """
        all_reviews = []
        continuation_token = None

        for _ in range(max_pages):
            result, continuation_token = reviews(
                app_id,
                lang="en",
                country="in",
                sort=Sort.NEWEST,
                count=200,
                continuation_token=continuation_token,
            )

            for r in result:
                text = r.get("content", "").strip()
                review_date = r.get("at").date()

                if text:
                    all_reviews.append({
                        "text": text,
                        "date": review_date
                    })

            if not continuation_token:
                break

        return all_reviews

    # INTERNAL: GROUP BY DATE
    def _group_by_date(self, reviews):
        grouped = defaultdict(list)

        for r in reviews:
            date_str = r["date"].strftime("%Y-%m-%d")
            grouped[date_str].append(r["text"])

        return grouped

    # PUBLIC API: FETCH DAILY REVIEWS
    def fetch_reviews(self, app_id, date_str):
        """
        Returns reviews for a specific date.
        Uses cached data to simulate daily batches.
        """

        # First-time fetch & cache
        if self.cached_reviews_by_date is None:
            print("📥 Fetching recent reviews from Play Store...")
            recent_reviews = self._fetch_recent_reviews(app_id)
            self.cached_reviews_by_date = self._group_by_date(recent_reviews)
            print(f"✅ Cached {sum(len(v) for v in self.cached_reviews_by_date.values())} reviews across {len(self.cached_reviews_by_date)} days")

        # Return only reviews for requested date
        return self.cached_reviews_by_date.get(date_str, [])

    # SAVE RAW REVIEWS
    def save_raw(self, reviews, date_str):
        if not reviews:
            print(f"No reviews found for {date_str}, skipping file write.")
            return

        os.makedirs("data/raw_reviews", exist_ok=True)
        df = pd.DataFrame({"review": reviews})

        file_path = f"data/raw_reviews/reviews_{date_str}.csv"
        df.to_csv(file_path, index=False)
