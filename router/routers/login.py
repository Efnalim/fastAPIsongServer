from __future__ import annotations
from typing import List

from fastapi import APIRouter, status, HTTPException

auth_router = APIRouter(tags=['auth'])

# @router.post('/subject', response_model=ApiResponse, tags=['subject'])
# def add_subject(
#     auth_token: str = Header(..., alias='auth-token'), body: SubjectBase = ...
# ) -> ApiResponse:
#     """
#     Add a new subject
#     """
#     handle_request(auth_token)
#     retval = Subject_service.add_subject(body)
#     if(retval):
#         return ApiResponse(code=202, type="success", message="Subject added successfully")
#     return ApiResponse(code=422, type="failure", message="Subject was not added")


# @router.put('/subject/{subject_id}', response_model=ApiResponse, tags=['subject'])
# def update_subject(
#     subject_id: str,
#     auth_token: str = Header(..., alias='auth-token'),
#     body: SubjectBase = ...,
# ) -> ApiResponse:
#     """
#     Update an existing subject
#     """
#     handle_request(auth_token)
#     retval = Subject_service.update_subject(subject_id , body)
#     if(retval):
#         return ApiResponse(code=200, type="success", message="Subject updated successfully")
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Subject not found",
#     )


# @router.delete('/subject/{subject_id}', response_model=ApiResponse, tags=['subject'])
# def delete_subject(
#     subject_id: str, auth_token: str = Header(..., alias='auth-token')
# ) -> ApiResponse:
#     """
#     Delete a subject
#     """
#     handle_request(auth_token)
#     retval = Subject_service.delete_subject(subject_id)
#     if(retval):
#         return ApiResponse(code=200, type="success", message="Subject deleted successfully")
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Subject not found",
#     )


# @router.get('/subject/{subject_id}', response_model=SubjectDetail, tags=['subject'])
# def get_subject_detail(
#     subject_id: str, auth_token: str = Header(..., alias='auth-token')
# ) -> SubjectDetail:
#     """
#     Get detail of a subject
#     """
#     handle_request(auth_token)
#     retval = Subject_service.get_subject_detail_by_id(subject_id, auth_token)
#     if(retval is not None):
#         return retval
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Subject not found",
#     )


@auth_router.get('/login', tags=['auth'])
def login(
) -> List:
    """
    Login
    """
    return ["login"]