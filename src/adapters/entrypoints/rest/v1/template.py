from pydantic import ValidationError
import yaml

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.utils.schemas import handler_schemas

router = APIRouter()


@router.get("/templates/validate")
async def template_validate(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        if file.content_type == "text/yaml" or file.content_type == "text/yml":
            parsed_file = yaml.safe_load(file.file.read())
            handler_schemas(parsed_file)
            file.file.close()
        else:
            raise Exception("Invalid file type")
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])

    return {"message": f"Successfully parserd {file.filename}"}
