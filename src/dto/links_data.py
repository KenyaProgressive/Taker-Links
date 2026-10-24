from pydantic import HttpUrl

from dto.base import DTO


class LinksDataDTO(DTO):
    _real_link: HttpUrl
    custom_len: int | None = None

    def get_str_link(self) -> str:
        return str(self._real_link)
