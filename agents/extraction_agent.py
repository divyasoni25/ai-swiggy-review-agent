import re

class ExtractionAgent:
    def __init__(self):

        # Canonical topic → keywords
        self.taxonomy = {
            "delivery delay": [
                "late", "delay", "not on time", "took long", "1 hour", "2 hours",
                "delivered late", "no update", "intentional delay"
            ],

            "cancellation fee": [
                "cancellation fee", "charged for cancel", "penalty", "fee charged"
            ],

            "refund not received": [
                "no refund", "not refunded", "refund not received",
                "money not returned", "refund denied"
            ],

            "wrong item delivered": [
                "wrong item", "different item", "not what i ordered",
                "sent something else", "order mismatch"
            ],

            "missing item": [
                "missing item", "items missing", "not included", "incomplete order"
            ],

            "food quality issue": [
                "cold food", "stale", "burnt", "tasteless",
                "bad taste", "quantity less", "spoiled"
            ],

            "double charged": [
                "charged twice", "double charged", "extra charge", "overcharged"
            ],

            "payment failure": [
                "payment failed", "payment deducted", "transaction failed"
            ],

            "app crash": [
                "app crash", "app not working", "screen blank", "app goes blank"
            ],

            "app performance issue": [
                "app is slow", "slow app", "lagging", "takes time", "loading"
            ],

            "app freeze": [
                "freezes", "screen stuck", "stuck", "hangs"
            ],

            "customer support unresponsive": [
                "no response", "no support", "no help", "ghosted",
                "no customer care", "support not responding"
            ],

            "no offers": [
                "no offers", "no discount", "no cashback", "offers not working"
            ],

            "instamart issue": [
                "instamart", "grocery", "wrong product"
            ],

            "wallet redemption issue": [
                "dinein cash", "cannot redeem", "cash expired",
                "redemption capped", "wallet limit"
            ],

            "pricing policy issue": [
                "cashback capped", "no value", "no benefit", "pricing policy"
            ],
        }

        self.sentiment_only = {
            "good", "very good", "nice", "awesome", "great",
            "bad", "worst", "ok", "okay", "super", "best",
            "love it", "amazing"
        }
        
        self.unmatched_phrases = []

    def extract_topics(self, reviews):
        all_topics = []
        self.unmatched_phrases = []

        for review in reviews:
            text = review.lower()

            clean = re.sub(r"[^\w\s]", " ", text).strip()
            if clean in self.sentiment_only:
                continue

            found = set()

            for canonical, keywords in self.taxonomy.items():
                for kw in keywords:
                    if kw in text:
                        found.add(canonical)
                        break

            if found:
                all_topics.extend(found)
            else:
                self.unmatched_phrases.append(clean)

        return all_topics, self.unmatched_phrases
