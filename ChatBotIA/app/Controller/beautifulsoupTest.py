from urllib.parse import urlparse
from requests import get
from fuzzywuzzy import process


class URLValidator:
    def __init__(self):
        pass

    def is_valid_url(self, url):
        """
        Verifica se a URL é válida e retorna uma mensagem de erro caso contrário.
        Também sugere uma URL correta, se possível.
        """
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            # Sugere adicionar o esquema
            if not parsed_url.scheme:
                http_url = "http://" + url
                https_url = "https://" + url
                if self.is_valid_url(http_url):
                    return f"URL inválida: esquema ausente. Tente {https_url}"
                if self.is_valid_url(https_url):
                    return f"URL inválida: esquema ausente. Tente {http_url}"
                else:
                    return "URL inválida: domínio ausente."

        try:
            https_url = "https://" + parsed_url.netloc + parsed_url.path
            response = get(https_url)
            if response.status_code == 200:
                return True
            else:
                # Se falhar, tenta com HTTP
                http_url = "http://" + parsed_url.netloc + parsed_url.path
                response = get(http_url)
                if response.status_code == 200:
                    return True
                else:
                    return f"Erro HTTP {response.status_code}: {response.reason}."
            
        except Exception as e:
            return f"Erro ao acessar a URL: {e}"

    def suggest_url(self, url):
        """
        Sugere uma URL correta com base na URL original.
        """
        parsed_url = urlparse(url)

        # Sugere correção de domínio usando fuzzy matching
        if parsed_url.netloc:
            known_domains = ["com", "net", "org", "gov", "edu", "br"]  # Lista expandida de domínios conhecidos
            closest_match = process.extractOne(parsed_url.netloc, known_domains)
            if closest_match and closest_match[1] >= 80:  # Ajuste o limite de semelhança se necessário
                suggested_url = parsed_url._replace(netloc=closest_match[0]).geturl()
                return suggested_url

        return None


validator = URLValidator()
while True:
    # Teste com algumas URLs
    urls = input("Digite a URL que deseja verificar: ").split()
    for url in urls:
        valid = validator.is_valid_url(url)
        suggestion = validator.suggest_url(url)
        print(f"{valid}")
        if suggestion:
            print(f"Sugestão: {suggestion}")
