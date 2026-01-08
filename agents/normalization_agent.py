import re

class NormalizationAgent:

    def __init__(self):
        # Canonical taxonomy
        self.allowed_topics = {
            "delivery delay",
            "delivery partner behavior",
            "order not delivered",
            "wrong item delivered",
            "missing item",
            "cold food",
            "refund not received",
            "double charged",
            "payment failure",
            "cancellation fee",
            "app crash",
            "login issue",
            "location error",
            "customer support unresponsive",
            "no resolution",
            "high prices",
            "no offers",
            "coupon not applied",
            "food quality issue",
            "instamart issue",
            "feature request",
            "app performance issue",
            "app freeze",
            "wallet redemption issue",
            "pricing policy issue",
        }

        # Variant → canonical mapping
        self.replacements = {
            "order delayed": "delivery delay",
            "late delivery": "delivery delay",
            "delivery late": "delivery delay",
            "took too long": "delivery delay",

            "food was cold": "cold food",
            "cold food": "cold food",
            "stale food": "food quality issue",
            "bad taste": "food quality issue",

            "refund not given": "refund not received",
            "no refund": "refund not received",
            "refund denied": "refund not received",

            "charged twice": "double charged",
            "extra charged": "double charged",
            "double payment": "double charged",

            "payment deducted": "payment failure",
            "payment failed": "payment failure",

            "app not working": "app crash",
            "app crash": "app crash",

            "login problem": "login issue",
            "cannot login": "login issue",

            "gps wrong": "location error",
            "wrong location": "location error",

            "no response from support": "customer support unresponsive",
            "support not responding": "customer support unresponsive",
            "no customer care": "customer support unresponsive",

            "too expensive": "high prices",
            "delivery charges high": "high prices",

            "no discount": "no offers",
            "no cashback": "no offers",

            "coupon not working": "coupon not applied",
            "offer not applied": "coupon not applied",

            "instamart problem": "instamart issue",
            "instamart issue": "instamart issue",
            
            # App performance / bugs
            "app is slow": "app performance issue",
            "slow app": "app performance issue",
            "lagging": "app performance issue",
            "freezes": "app freeze",
            "screen stuck": "app freeze",

            # Wrong / mismatched order
            "wrong item": "wrong item delivered",
            "sent something else": "wrong item delivered",
            "got different item": "wrong item delivered",
            "not what i ordered": "wrong item delivered",
            "order mismatch": "wrong item delivered",

            # Wallet / dine-in issues
            "dinein cash": "wallet redemption issue",
            "cannot redeem": "wallet redemption issue",
            "cash expired": "wallet redemption issue",
            "redemption capped": "wallet redemption issue",
            "wallet limit": "wallet redemption issue",

            # Policy / pricing constraints
            "no value": "pricing policy issue",
            "no benefit": "pricing policy issue",
            "cashback capped": "pricing policy issue",

        }

        # Sentiment / junk phrases
        self.blocklist = {
            "good", "very good", "nice", "awesome", "great", "bad", "worst",
            "i like it", "that's good", "very nice", "amazing", "love it",
            "ok", "okay", "super", "best", "fine", "better now"
        }

        # Meta / non-issue labels
        self.meta_patterns = [
            "review", "user issues", "user reviews",
            "positive experiences", "specific user problems",
            "feedback", "comments"
        ]

    # TEXT NORMALIZATION
    def normalize_text(self, text):
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Collapse variants
        for k, v in self.replacements.items():
            if k in text:
                return v

        return text

    # VALIDATION
    def is_valid_topic(self, topic):
        if not topic:
            return False

        # Reject long sentences
        if len(topic.split()) > 6:
            return False

        # Reject sentiment-only
        if topic in self.blocklist:
            return False

        # Reject meta labels
        for pat in self.meta_patterns:
            if pat in topic:
                return False

        # Only allow taxonomy categories
        if topic not in self.allowed_topics:
            return False

        return True

    # FINAL NORMALIZATION
    def normalize_topic(self, new_embedding, new_topic, existing_topics):
        """
        Taxonomy-enforced normalization.
        No semantic similarity needed anymore.
        """

        # Since taxonomy is enforced, canonical topic is the topic itself
        return new_topic
