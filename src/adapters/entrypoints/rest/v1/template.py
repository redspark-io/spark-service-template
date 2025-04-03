from pydantic import ValidationError
from sqlalchemy.engine import mock
import yaml

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.domain.exceptions.template_exceptions import TemplateInvalidFileTypeException
from src.utils.template_schema_factory import create_template_schema

router = APIRouter()

MOCKING_PARSED_FILE = {
    "apiVersion": "v1beta1",
    "kind": "Template",
    "metadata": {
        "name": "template-test",
        "title": "Template Test",
        "description": "Template teste",
        "tags": ["test", "template"],
    },
    "spec": {
        "type": "service",
        "parameters": [
            {
                "title": "Form 1",
                "required": ["field1"],
                "properties": {
                    "field1": {
                        "title": "Field 1",
                        "type": "string",
                        "description": "Field 1 description",
                    },
                    "field2": {
                        "title": "Field 2",
                        "type": "string",
                        "description": "Field 2 description",
                    },
                },
            },
        ],
        "steps": [
            {
                "id": "step1",
                "name": "Step 1",
                "action": "fetch:template",
                "input": {"value1": "${value1}"},
            },
            {
                "id": "step2",
                "name": "Step 2",
                "action": "fetch:template",
                "input": {"value1": "${value1}"},
            }
        ],
    },
}

@router.get("/templates/validate")
async def template_validate(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    API GET to Validate template
    """

    try:
        if file.content_type == "text/yaml" or file.content_type == "text/yml":
            parsed_file = yaml.safe_load(file.file.read())
            create_template_schema(parsed_file)
        else:
            raise TemplateInvalidFileTypeException
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    finally:
        file.file.close()

    return {"message": f"Successfully parserd {file.filename}"}


@router.post("/templates/{template_id}/run")
async def template_run(template_id: str, form: dict, db: AsyncSession = Depends(get_db)):
    """
    API POST to Run template
    """

    # TODO: need recovery parsed template.yaml file from service hub, but for now mocking
    template_schema = create_template_schema(MOCKING_PARSED_FILE) 
    required_fields = []
    for parameter in template_schema.spec.parameters:
        if parameter.required:
            required_fields.extend(parameter.required)

    missing_fields = []
    for required_field in required_fields:
        if required_field not in form or not form[required_field]:
            missing_fields.append(required_field)

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field(s): {', '.join(missing_fields)}",
        )

    for step in template_schema.spec.steps:
        print(step.id)

    return {"message": f"Successfully run template {template_id}"}
