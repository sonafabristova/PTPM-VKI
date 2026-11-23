import requests
from bs4 import BeautifulSoup


class ForumParser:
    BASE_URL = "https://quotes.toscrape.com"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def parse_page(self, url: str):
        response = requests.get(url, headers=self.HEADERS, timeout=10)
        response.raise_for_status()
        return self.parse_html(response.text)

    def parse_html(self, html: str):
        soup = BeautifulSoup(html, "lxml")
        results = []

        for idx, quote_div in enumerate(soup.select("div.quote"), start=1):
            message_div = quote_div.select_one("span.text")
            author_div = quote_div.select_one("small.author")

            if message_div is None or author_div is None:
                continue

            message = str(message_div)
            author = author_div.get_text(strip=True)

            comment_id = self._extract_id(quote_div, fallback=idx)
            results.append({
                "id": comment_id,
                "name": author,
                "message": message,
            })

        return results

    def _extract_id(self, tag, fallback: int) -> int:
        for attr in ("data-id", "id"):
            value = tag.get(attr)
            if value and str(value).isdigit():
                return int(value)

        link = tag.select_one("a[href]")
        if link:
            href = link.get("href", "")
            for part in href.replace("/", " ").replace("#", " ").split():
                if part.isdigit():
                    return int(part)

        return fallback

    def save_to_db(self, parsed_data, repository) -> int:
        saved = 0
        for item in parsed_data:
            try:
                repository.add(item["id"], item["name"], item["message"])
                saved += 1
            except ValueError:
                continue
        return saved