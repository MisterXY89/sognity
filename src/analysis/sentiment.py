
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def _prep_lyrics(self, lyrics):
        lyrics = ";".join(lyrics.split("\n"))
        lyrics = "".join(lyrics.split("[Intro]"))
        lyrics = "".join(lyrics.split("[Outro]"))
        lyrics = "".join(lyrics.split("[Chorus]"))
        lyrics = "".join(lyrics.split("[Pre-Chorus]"))
        lyrics = "".join(lyrics.split("[Post-Chorus]"))
        lyrics = "".join(lyrics.split("[Bridge]"))
        lyrics = "".join(lyrics.split("[Verse 1]"))
        lyrics = "".join(lyrics.split("[Verse 2]"))
        lyrics = "".join(lyrics.split("[Verse 3]"))
        lyrics = "".join(lyrics.split("[Verse 4]"))
        lyrics = "".join(lyrics.split("[Verse 5]"))
        lyrics = "".join(lyrics.split("[Verse 6]"))
        lyrics = "".join(lyrics.split("[Verse 7]"))
        lyrics = lyrics.replace("<br>", " ")
        if lyrics[0] == ";":
            lyrics = lyrics[1:]
        return lyrics

    def get_scores(self, lyrics):
        prepped = self._prep_lyrics(lyrics)
        return self.analyzer.polarity_scores(prepped)

    def get_sentiment_string(self, pol_scores):
        comp = pol_scores["compound"]
        if comp >= 0.05:
            return "positive"
        elif comp <= -0.05:
            return "negative"
        return "neutral"
