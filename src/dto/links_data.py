from pydantic import HttpUrl

from dto.base import DTO


class LinksDataDTO(DTO):
    real_link: HttpUrl
    custom_len: int | None = None

    def get_str_link(self) -> str:
        return str(self.real_link)
