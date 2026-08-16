from ...dependencies import get_subject_service


def create_subject(name: str, code: str):
    subject_service = get_subject_service()

    subject = subject_service.create_subject(name, code)

    if not subject:
        raise Exception("Failed to create subject")

    return {
        "id": subject.id,
        "name": subject.name,
        "code": subject.code,
    }
