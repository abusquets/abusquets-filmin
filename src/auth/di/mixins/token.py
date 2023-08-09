from auth.domain.services.token import TokenService


class TokenContainerMixin:
    token_service: TokenService

    def _get_token_service(self) -> TokenService:
        return TokenService()
