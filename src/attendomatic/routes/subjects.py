# Routes for subjects CRUD operations

from fastapi import APIRouter, Depends, HTTPException, status

from attendomatic.request_schema.subject import (
    CreateSubjectRequest,
    DeleteSubjectRequest,
    UpdateSubjectRequest,
)
from ..dependencies import get_subject_service, get_user_service, admin_required

router = APIRouter()


# ============ READ ENDPOINTS ============


@router.get("/subjects", status_code=status.HTTP_200_OK)
async def get_all_subjects(
    subject_service=Depends(get_subject_service),
):
    """Get all subjects (public read)"""
    return subject_service.get_all_subjects()


@router.get("/subjects/{subject_id}", status_code=status.HTTP_200_OK)
async def get_subject_by_id(
    subject_id: int,
    subject_service=Depends(get_subject_service),
):
    """Get subject by ID"""
    subject = subject_service.get_subject_by_id(subject_id)

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return subject


@router.get("/subjects/code/{code}", status_code=status.HTTP_200_OK)
async def get_subject_by_code(
    code: str,
    subject_service=Depends(get_subject_service),
):
    """Get subject by code"""
    subject = subject_service.get_subject_by_code(code)

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return subject


# ============ WRITE ENDPOINTS (require admin) ============


@router.post("/create_subject", status_code=status.HTTP_201_CREATED)
async def create_subject(
    request: CreateSubjectRequest,
    subject_service=Depends(get_subject_service),
    user_service=Depends(get_user_service),
):
    """Create a new subject (admin only)"""

    # Authorization check
    user = user_service.get_user_by_email(request.user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Admin access required",
        )

    # Create subject
    subject = subject_service.create_subject(
        request.name,
        request.code,
    )

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subject",
        )

    return subject


@router.put("/update_subject", status_code=status.HTTP_200_OK)
async def update_subject(
    request: UpdateSubjectRequest,
    subject_service=Depends(get_subject_service),
    user_service=Depends(get_user_service),
):
    """Update an existing subject (admin only)"""

    # Authorization check
    user = user_service.get_user_by_email(request.user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Admin access required",
        )

    # Check if subject exists
    subject = subject_service.get_subject_by_id(subject_id)

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Update subject
    updated_subject = subject_service.update_subject(
        subject_id,
        request.name,
        request.code,
    )

    if not updated_subject:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update subject",
        )

    return updated_subject


@router.delete("/delete_subject", status_code=status.HTTP_200_OK)
async def delete_subject(
    request: DeleteSubjectRequest,
    subject_service=Depends(get_subject_service),
    user_service=Depends(get_user_service),
):
    """Delete a subject (admin only)"""

    # Authorization check
    user = user_service.get_user_by_email(request.user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Admin access required",
        )

    # Check if subject exists
    subject = subject_service.get_subject_by_id(subject_id)

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    # Delete subject
    deleted = subject_service.delete_subject(subject_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete subject",
        )

    return {"message": "Subject deleted successfully"}
