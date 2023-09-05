from django.shortcuts import render
from rest_framework import viewsets
from .models import Server
from .serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        """This method starts by extracting the query params from the request,
        the values are assigned to the variables category, qty, by_user, by_serverid, and
        with_num_members.
        It checks to see if the user is authenticated, if not, it raises an AuthenticationFailed
        Then, it filters the queryset based on these variables (one after the other if they are defined).
        THen it is annotated with the num_members of each server.
        if the qty is provided, query set is sliced to include only the specified qty.
        Finally, it serializes the queryset and returns it."""
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if with_num_members:
            # count the number of members in each server
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            try:
                self.queryset = self.queryset.get(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(detail=f"Server with id {by_serverid} not found")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        return Response(serializer.data)
