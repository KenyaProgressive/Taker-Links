from typing import Annotated

from fastapi import Depends

from services.links_data_service import LinksDataService

LinksDataServiceDep = Annotated[LinksDataService, Depends(LinksDataService)]
