class UrlOperator:

    @staticmethod
    def normalize_url(url):
        """Normalize the URL to create a safe filename."""
        # Remove the protocol part and replace special characters
        normalized_url = url.replace("://", "_").replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
        return normalized_url
