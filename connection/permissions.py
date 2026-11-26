
from rest_framework.permissions import BasePermission 


class IsParticipant(BasePermission):
    """
    Only authenticated participants can access the resource.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "participant"
        )


class IsCoachOrAdmin(BasePermission):
    """
    Coaches and administrators can access management resources.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["coach", "admin"]
        )


class IsAdmin(BasePermission):
    """
    Only administrators can access this resource.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsOwnerOrCoachOrAdmin(BasePermission):
    """
    Participants can access their own records.
    Coaches and administrators can access records
    according to the relevant management workflow.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.role == "admin":
            return True

        if request.user.role == "coach":
            return True

        owner = getattr(obj, "user", None)

        if owner is None:
            owner = getattr(obj, "participant", None)

        return owner == request.user


class CanReviewAssessment(BasePermission):
    """
    Participants can view their own assessment.
    Coaches and administrators can review assessments.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.role in ["coach", "admin"]:
            return True

        return obj.participant_id == request.user.pk
