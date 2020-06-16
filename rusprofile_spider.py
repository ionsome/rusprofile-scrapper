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
        """Парсит страницы каталога ОКВЭД.

        Парсит каталог постранично, для каждой компании
        вызывает self.parse_company_page.
    
        """
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
        """Парсинг страницу компании.

        Все данные приводятся к виду в таблице.
        
        Также проверяет валидность ОГРН:
        при скрапинге сервер генерирует капчу с рандомными данными.

        """
        data = {
            'ogrn': response.xpath(
                '//*[@id="clip_ogrn"]/text()',
            ).get(),
            'name': response.css('div.company-name::text').get().strip(),
            'okpo': response.css('#clip_okpo::text').get(),
            'current_status': self.handle_status(
                response.css('div.company-status').attrib['class'],
            ),
            'reg_date': self.handle_reg_date(
                response.xpath(
                    '//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[1]/dd/text()',
                ).get(),
            ),
            'auth_capital': self.handle_auth_capital(
                response.xpath(
                    '//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[2]/dd/span/text()',
                ).get()
            ),
        }

        if self.validate_ogrn(data['ogrn']):
            yield data
        else:
            self.logger.error('\ninvalid identifier %s\n', data['ogrn'])

    @staticmethod
    def validate_ogrn(ogrn):
        """Валидация ОГРН.
        
        Returns:
            Логическое значение.
    
        Examples:
            >>> RusprofileSpider.validate_ogrn('1202700008378')
            True
            >>> RusprofileSpider.validate_ogrn('1126330000060')
            True
            >>> RusprofileSpider.validate_ogrn('8664911781082')
            False

        """
        if not ogrn:
            return False
        if len(ogrn) == 13:
            delimeter = 11
        elif len(ogrn) == 15:
            delimeter = 13
        else:
            return False
        main_part = int(ogrn[:-1]) % delimeter % 10
        checksum = int(ogrn[-1])

        return main_part == checksum

    @staticmethod
    def handle_status(classes):
        """Обрабатывает значение со статусом компании.

        Значение выбирается из _STATUS_MAP.

        Returns:
            Строка.

        Examples:
            >>> RusprofileSpider.handle_status('status active-yes')
            'действующая'

        """
        _value = classes.split()[-1]
        return _STATUS_MAP.get(_value)

    @staticmethod
    def handle_reg_date(date):
        """Обрабатывает значение с датой регистрации.

        Returns:
            Строка вида YYYYMMDD.

        Examples:
            >>> RusprofileSpider.handle_reg_date('21.02.1997')
            '19970221'

        """
        date = date.split('.')[::-1]
        return ''.join(date)

    @staticmethod
    def handle_auth_capital(capital):
        """Обрабатывает значение условной капитализации.

        Пример: "10 000 руб." => 10000.

        Returns:
            Целое число или None.

        Examples:
            >>> RusprofileSpider.handle_auth_capital(None)
            >>> RusprofileSpider.handle_auth_capital('10 000 руб.')
            10000

        """
        if capital:
            capital = int(''.join(capital[:-4].split()))
        return capital
