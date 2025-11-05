import scrapy

class OcsinfoSpider(scrapy.Spider):
    name = 'ocsinfo'
    allowed_domains = ['192.168.0.241']
    start_urls = ['http://192.168.0.241/ocsreports/index.php']

    def parse(self, response):
        data = {
            "LOGIN": "garbuio",
            "PASSWD": "1nv3nt2r10*G@rbu10",
            "Valid_CNX": "Enviar",
        }
        return scrapy.FormRequest(
            "http://192.168.0.241/ocsreports/index.php",
            self.parse_login,
            formdata=data,
        )

    def parse_login(self, response):                    
        # Download csv
        return scrapy.Request(
            "http://192.168.0.241/ocsreports/index.php?function=visu_computers",
            self.parse_visu_computers,
        )
    
    def parse_visu_computers(self, response):
        return scrapy.FormRequest.from_response(
            response,
            url="http://192.168.0.241/ocsreports/ajax.php?function=visu_computers&no_header=true&no_footer=true",
            callback=self.parse_all_computers,
            formid="show_all",
            formdata={
                'start': '0',
                'length': '1000',
            }
        )
        
    def parse_all_computers(self, response):
        for computer in response.json()["data"]:
            yield response.follow(
                f"index.php?function=computer&head=1&systemid={computer['ID']}",
                self.parse_computer,
            )
        
    def parse_computer(self, response):
        result = {
            "url": response.url,
        }
        for title, value in zip(
            response.css("span.summary-header::text").getall(),
            response.css("span.summary-value::text").getall()
        ):
            result[title.lower().strip(": ")] = value
        return result
    
