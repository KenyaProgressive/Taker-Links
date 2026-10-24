from dto.base import DTO

class LinksDataDTO(DTO):
    real_link: str
    custom_len: int | None = None