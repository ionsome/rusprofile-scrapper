import scrapy

_STATUS_MAP = {
    'active-yes': 'действующая',
    'reorganizated': 'в процессе ликвидации',
    'deleted': 'ликвидирована',
}


class RusprofileSpider(scrapy.Spider):
    """Spider class для компаний на rusprofile.ru.

    Парсинг компаний происходит по кодам ОКВЭД.

    Attributes:
        name: Имя бота.
        start_urls: Начальные urls.

    """

    name = 'rusprofile'

    def __init__(self, ids=[], *args, **kwargs):
        """Инициализация бота.

        Args:
            ids: Список кодов ОКВЭД.

        """
        super().__init__(*args, **kwargs)
        self.start_urls = [
            f'https://www.rusprofile.ru/codes/{_id}' for _id in ids
        ]

    def parse(self, response):
        for company in response.css('div.company-item'):
            company_page = company.css(
                'div.company-item__title a::attr("href")').get()
            yield response.follow(
                company_page,
                callback=self.parse_company_page,
            )

        next_page = response.css('a.nav-next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_company_page(self, response):
        yield {
            'name': response.css('div.company-name::text').get().strip(),
            'ogrn': response.css('#clip_ogrn::text').get(),
            'okpo': response.xpath('//*[@id="anketa"]/div[2]/div[2]/dl/dd[1]/span[1]/text()').get(),
            'status': self._get_company_status(response.css('div.company-status')),
            'reg_date': response.xpath('//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[1]/dd/text()').get(),
            'auth_capital': response.xpath('//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[2]/dd/span/text()').get(),
        }

    def _get_company_status(self, node):
        value = node.attrib['class'].split()[-1]
        return _STATUS_MAP.get(value)
