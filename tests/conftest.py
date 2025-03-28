import pytest


@pytest.fixture
def parserd_file_v1beta1():
    return {
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
                }
            ],
        },
    }


@pytest.fixture
def parserd_file_v1beta2():
    return {
        "apiVersion": "v1beta2",
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
                }
            ],
        },
    }
